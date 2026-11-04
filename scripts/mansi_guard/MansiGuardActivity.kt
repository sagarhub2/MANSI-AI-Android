package com.jarvis.assistant.ui.security

import android.os.Bundle
import android.text.InputType
import android.widget.Button
import android.widget.EditText
import android.widget.TextView
import android.widget.Toast
import androidx.appcompat.app.AlertDialog
import androidx.appcompat.app.AppCompatActivity
import androidx.core.content.ContextCompat
import com.jarvis.assistant.R
import com.jarvis.assistant.background.MansiGuardService
import java.security.MessageDigest

class MansiGuardActivity : AppCompatActivity() {
    private val prefs by lazy { getSharedPreferences("mansi_guard", MODE_PRIVATE) }
    private lateinit var status: TextView
    private lateinit var action: Button

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_mansi_guard)
        status = findViewById(R.id.tvGuardStatus)
        action = findViewById(R.id.btnGuardAction)
        findViewById<Button>(R.id.btnGuardBack).setOnClickListener { finish() }
        action.setOnClickListener {
            if (prefs.getBoolean("guard_active", false)) disarmDialog() else setupPinDialog()
        }
        refresh()
    }

    override fun onResume() { super.onResume(); refresh() }

    private fun refresh() {
        val active = prefs.getBoolean("guard_active", false)
        status.text = if (active) "GUARD ACTIVE • PHONE PROTECTED" else "GUARD STANDBY • NOT PROTECTED"
        action.text = if (active) "DISARM WITH PIN" else "ACTIVATE GUARD"
    }

    private fun pinField() = EditText(this).apply {
        inputType = InputType.TYPE_CLASS_NUMBER or InputType.TYPE_NUMBER_VARIATION_PASSWORD
        hint = "4–8 digit PIN"
        setSingleLine(true)
    }

    private fun setupPinDialog() {
        val field = pinField()
        AlertDialog.Builder(this).setTitle("Create Guard PIN")
            .setMessage("Choose a private 4–8 digit PIN. You will need it to disarm MANSI GUARD.")
            .setView(field).setNegativeButton("Cancel", null)
            .setPositiveButton("Save & Activate") { _, _ ->
                val pin = field.text.toString()
                if (pin.length !in 4..8 || !pin.all { it.isDigit() }) {
                    Toast.makeText(this, "Enter a 4–8 digit PIN", Toast.LENGTH_LONG).show()
                } else {
                    prefs.edit().putString("pin_hash", hash(pin)).putBoolean("guard_active", true).apply()
                    ContextCompat.startForegroundService(
                        this, android.content.Intent(this, MansiGuardService::class.java).setAction(MansiGuardService.ACTION_ARM)
                    )
                    Toast.makeText(this, "MANSI GUARD armed. Lock your phone now.", Toast.LENGTH_LONG).show()
                    finish()
                }
            }.show()
    }

    private fun disarmDialog() {
        val field = pinField()
        AlertDialog.Builder(this).setTitle("Disarm MANSI GUARD")
            .setMessage("Enter your Guard PIN to stop monitoring and silence the alarm.")
            .setView(field).setNegativeButton("Cancel", null)
            .setPositiveButton("Disarm") { _, _ ->
                if (hash(field.text.toString()) == prefs.getString("pin_hash", null)) {
                    prefs.edit().putBoolean("guard_active", false).apply()
                    startService(android.content.Intent(this, MansiGuardService::class.java).setAction(MansiGuardService.ACTION_DISARM))
                    Toast.makeText(this, "MANSI GUARD disarmed", Toast.LENGTH_SHORT).show()
                    refresh()
                } else Toast.makeText(this, "Incorrect PIN", Toast.LENGTH_SHORT).show()
            }.show()
    }

    private fun hash(value: String): String =
        MessageDigest.getInstance("SHA-256").digest(value.toByteArray(Charsets.UTF_8))
            .joinToString("") { "%02x".format(it) }
}