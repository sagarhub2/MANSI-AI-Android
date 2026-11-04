package com.jarvis.assistant.background

import android.app.NotificationChannel
import android.app.NotificationManager
import android.app.PendingIntent
import android.app.Service
import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent
import android.content.IntentFilter
import android.content.pm.ServiceInfo
import android.hardware.Sensor
import android.hardware.SensorEvent
import android.hardware.SensorEventListener
import android.hardware.SensorManager
import android.media.AudioManager
import android.media.ToneGenerator
import android.os.Build
import android.os.Handler
import android.os.IBinder
import android.os.Looper
import android.os.VibrationEffect
import android.os.Vibrator
import android.os.VibratorManager
import androidx.core.app.NotificationCompat
import androidx.core.app.ServiceCompat
import com.jarvis.assistant.R
import com.jarvis.assistant.ui.security.MansiGuardActivity
import kotlin.math.sqrt

/** User-armed foreground anti-theft monitor. Android does not expose every global touch event to normal apps. */
class MansiGuardService : Service(), SensorEventListener {
    companion object {
        const val ACTION_ARM = "com.jarvis.assistant.guard.ARM"
        const val ACTION_DISARM = "com.jarvis.assistant.guard.DISARM"
        const val EXTRA_PIN_HASH = "pin_hash"
        private const val CHANNEL = "mansi_guard_security"
        private const val NOTIFICATION_ID = 7319
    }

    private val prefs by lazy { getSharedPreferences("mansi_guard", MODE_PRIVATE) }
    private lateinit var sensors: SensorManager
    private var receiver: BroadcastReceiver? = null
    private var receiverRegistered = false
    private var tone: ToneGenerator? = null
    private val handler = Handler(Looper.getMainLooper())
    private var armedAt = 0L
    private var alarmActive = false
    private var gravity = FloatArray(3)
    private val sirenLoop = object : Runnable {
        override fun run() {
            if (!alarmActive || !isArmed()) return
            try {
                if (tone == null) tone = ToneGenerator(AudioManager.STREAM_ALARM, 100)
                tone?.startTone(ToneGenerator.TONE_CDMA_ALERT_CALL_GUARD, 7000)
            } catch (_: Exception) { }
            handler.postDelayed(this, 7200L)
        }
    }

    override fun onCreate() {
        super.onCreate()
        createChannel()
        sensors = getSystemService(SENSOR_SERVICE) as SensorManager
        val filter = IntentFilter().apply {
            addAction(Intent.ACTION_SCREEN_ON)
            addAction(Intent.ACTION_POWER_DISCONNECTED)
        }
        receiver = object : BroadcastReceiver() {
            override fun onReceive(context: Context?, intent: Intent?) {
                if (!isArmed() || System.currentTimeMillis() - armedAt < 5000L) return
                when (intent?.action) {
                    Intent.ACTION_SCREEN_ON -> alert("Screen woke while Guard was armed")
                    Intent.ACTION_POWER_DISCONNECTED -> alert("Charger disconnected")
                }
            }
        }
        if (Build.VERSION.SDK_INT >= 33) registerReceiver(receiver, filter, Context.RECEIVER_NOT_EXPORTED)
        else @Suppress("DEPRECATION") registerReceiver(receiver, filter)
        receiverRegistered = true
    }

    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        when (intent?.action) {
            ACTION_ARM -> {
                prefs.edit().putBoolean("guard_active", true).apply()
                armedAt = System.currentTimeMillis()
                alarmActive = false
            }
            ACTION_DISARM -> {
                val supplied = intent.getStringExtra(EXTRA_PIN_HASH)
                if (supplied != null && supplied == prefs.getString("pin_hash", null)) {
                    disarm()
                    return START_NOT_STICKY
                }
                if (!isArmed()) { disarm(); return START_NOT_STICKY }
            }
        }
        if (!isArmed()) { stopSelf(); return START_NOT_STICKY }
        val notification = buildNotification()
        if (Build.VERSION.SDK_INT >= 29) {
            ServiceCompat.startForeground(this, NOTIFICATION_ID, notification, ServiceInfo.FOREGROUND_SERVICE_TYPE_MEDIA_PLAYBACK)
        } else startForeground(NOTIFICATION_ID, notification)
        sensors.getDefaultSensor(Sensor.TYPE_ACCELEROMETER)?.let {
            sensors.registerListener(this, it, SensorManager.SENSOR_DELAY_NORMAL)
        }
        return START_STICKY
    }

    override fun onSensorChanged(event: SensorEvent?) {
        if (event?.sensor?.type != Sensor.TYPE_ACCELEROMETER || !isArmed() || alarmActive) return
        if (System.currentTimeMillis() - armedAt < 5000L) return
        val alpha = 0.8f
        for (i in 0..2) gravity[i] = alpha * gravity[i] + (1f - alpha) * event.values[i]
        val x = event.values[0] - gravity[0]
        val y = event.values[1] - gravity[1]
        val z = event.values[2] - gravity[2]
        if (sqrt(x*x + y*y + z*z) > 3.2f) alert("Phone movement detected")
    }

    override fun onAccuracyChanged(sensor: Sensor?, accuracy: Int) = Unit

    private fun alert(reason: String) {
        if (!isArmed() || alarmActive) return
        alarmActive = true
        val notification = NotificationCompat.Builder(this, CHANNEL)
            .setSmallIcon(R.drawable.ic_settings_shield)
            .setContentTitle("MANSI GUARD • SECURITY ALERT")
            .setContentText(reason)
            .setOngoing(true)
            .setPriority(NotificationCompat.PRIORITY_MAX)
            .setCategory(NotificationCompat.CATEGORY_ALARM)
            .build()
        (getSystemService(NOTIFICATION_SERVICE) as NotificationManager).notify(NOTIFICATION_ID, notification)
        try {
            tone = ToneGenerator(AudioManager.STREAM_ALARM, 100)
            handler.removeCallbacks(sirenLoop)
            handler.post(sirenLoop)
        } catch (_: Exception) { }
        val pattern = longArrayOf(0, 500, 250, 500, 250, 900)
        try {
            if (Build.VERSION.SDK_INT >= 31) {
                (getSystemService(VIBRATOR_MANAGER_SERVICE) as VibratorManager).defaultVibrator
                    .vibrate(VibrationEffect.createWaveform(pattern, 0))
            } else {
                @Suppress("DEPRECATION")
                (getSystemService(VIBRATOR_SERVICE) as Vibrator).vibrate(VibrationEffect.createWaveform(pattern, 0))
            }
        } catch (_: Exception) { }
    }

    private fun disarm() {
        prefs.edit().putBoolean("guard_active", false).apply()
        alarmActive = false
        handler.removeCallbacks(sirenLoop)
        try { tone?.stopTone(); tone?.release() } catch (_: Exception) { }
        tone = null
        try {
            if (Build.VERSION.SDK_INT >= 31) (getSystemService(VIBRATOR_MANAGER_SERVICE) as VibratorManager).defaultVibrator.cancel()
            else @Suppress("DEPRECATION") (getSystemService(VIBRATOR_SERVICE) as Vibrator).cancel()
        } catch (_: Exception) { }
        sensors.unregisterListener(this)
        stopForeground(STOP_FOREGROUND_REMOVE)
        stopSelf()
    }

    private fun isArmed() = prefs.getBoolean("guard_active", false)

    private fun buildNotification() = NotificationCompat.Builder(this, CHANNEL)
        .setSmallIcon(R.drawable.ic_settings_shield)
        .setContentTitle("MANSI GUARD is active")
        .setContentText("Monitoring movement, screen wake and charger removal")
        .setContentIntent(PendingIntent.getActivity(this, 1, Intent(this, MansiGuardActivity::class.java),
            PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE))
        .setOngoing(true)
        .setCategory(NotificationCompat.CATEGORY_SERVICE)
        .setPriority(NotificationCompat.PRIORITY_HIGH)
        .build()

    private fun createChannel() {
        if (Build.VERSION.SDK_INT >= 26) {
            val channel = android.app.NotificationChannel(CHANNEL, "MANSI GUARD", NotificationManager.IMPORTANCE_HIGH)
            channel.description = "MANSI AI anti-theft alerts"
            (getSystemService(NOTIFICATION_SERVICE) as NotificationManager).createNotificationChannel(channel)
        }
    }

    override fun onDestroy() {
        sensors.unregisterListener(this)
        handler.removeCallbacks(sirenLoop)
        if (receiverRegistered) try { unregisterReceiver(receiver) } catch (_: Exception) { }
        try { tone?.stopTone(); tone?.release() } catch (_: Exception) { }
        super.onDestroy()
    }

    override fun onBind(intent: Intent?): IBinder? = null
}