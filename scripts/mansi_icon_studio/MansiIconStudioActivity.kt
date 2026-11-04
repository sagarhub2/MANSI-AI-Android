package com.jarvis.assistant.ui.tools

import android.app.Activity
import android.content.Intent
import android.content.pm.ShortcutInfo
import android.content.pm.ShortcutManager
import android.graphics.Bitmap
import android.graphics.BitmapFactory
import android.graphics.Canvas
import android.graphics.Paint
import android.graphics.Path
import android.graphics.LinearGradient
import android.graphics.Shader
import android.graphics.Color
import android.graphics.drawable.BitmapDrawable
import android.graphics.drawable.GradientDrawable
import android.graphics.drawable.Icon
import android.net.Uri
import android.os.Build
import android.os.Bundle
import android.provider.MediaStore
import android.view.Gravity
import android.view.View
import android.widget.Button
import android.widget.ImageView
import android.widget.LinearLayout
import android.widget.ScrollView
import android.widget.TextView
import android.widget.Toast
import androidx.activity.ComponentActivity
import androidx.activity.result.contract.ActivityResultContracts
import java.io.ByteArrayOutputStream
import java.io.OutputStream

class MansiIconStudioActivity : ComponentActivity() {
    private var chosenBitmap: Bitmap? = null
    private var selectedA = Color.rgb(25, 105, 255)
    private var selectedB = Color.rgb(190, 65, 255)
    private lateinit var preview: ImageView
    private lateinit var previewBg: GradientDrawable

    private val gallery = registerForActivityResult(ActivityResultContracts.GetContent()) { uri: Uri? ->
        if (uri != null) {
            try {
                contentResolver.openInputStream(uri)?.use { chosenBitmap = BitmapFactory.decodeStream(it) }
                renderPreview()
            } catch (_: Exception) {
                Toast.makeText(this, "Image open nahi ho paayi", Toast.LENGTH_SHORT).show()
            }
        }
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        buildScreen()
    }

    private fun dp(v: Int) = (v * resources.displayMetrics.density).toInt()
    private fun label(value: String, size: Float = 15f): TextView = TextView(this).apply {
        text = value; textSize = size; setTextColor(Color.WHITE)
    }

    private fun buildScreen() {
        val root = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            setPadding(dp(20), dp(18), dp(20), dp(24))
            setBackgroundColor(Color.rgb(10, 10, 24))
        }
        val scroll = ScrollView(this)
        val content = LinearLayout(this).apply { orientation = LinearLayout.VERTICAL }
        content.addView(label("MANSI ICON STUDIO 🎨", 23f))
        content.addView(label("Apna icon banao • preview dekho • save karo", 13f).apply {
            setTextColor(Color.LTGRAY); setPadding(0, dp(6), 0, dp(18))
        })

        previewBg = GradientDrawable(GradientDrawable.Orientation.TL_BR, intArrayOf(selectedA, selectedB)).apply {
            cornerRadius = dp(30).toFloat()
        }
        preview = ImageView(this).apply {
            scaleType = ImageView.ScaleType.CENTER_CROP
            background = previewBg
            clipToOutline = true
            setPadding(dp(18), dp(18), dp(18), dp(18))
        }
        val previewWrap = LinearLayout(this).apply {
            gravity = Gravity.CENTER
            setPadding(0, dp(12), 0, dp(22))
            addView(preview, LinearLayout.LayoutParams(dp(190), dp(190)))
        }
        content.addView(previewWrap)

        content.addView(label("1. Gallery se image choose karo"))
        content.addView(actionButton("Choose from Gallery") { gallery.launch("image/*") })
        content.addView(label("2. Background colours", 16f).apply { setPadding(0, dp(18), 0, dp(8)) })
        val colors = listOf(
            "Blue + Purple" to (Color.rgb(25,105,255) to Color.rgb(190,65,255)),
            "Pink + Violet" to (Color.rgb(255,70,160) to Color.rgb(120,65,255)),
            "Aqua + Blue" to (Color.rgb(0,205,190) to Color.rgb(25,105,255)),
            "Black + Gold" to (Color.rgb(25,22,18) to Color.rgb(220,165,55)),
            "Sunset" to (Color.rgb(255,110,65) to Color.rgb(255,55,145))
        )
        colors.forEach { (name, pair) ->
            content.addView(actionButton(name) {
                selectedA = pair.first; selectedB = pair.second; renderPreview()
            })
        }
        content.addView(label("3. Save / apply", 16f).apply { setPadding(0, dp(18), 0, dp(8)) })
        content.addView(actionButton("Save Icon PNG") { savePng() })
        content.addView(actionButton("Add Custom Icon to Home Screen") { pinCustomShortcut() })
        content.addView(label("Note: Android security ke kaaran custom image se original app-drawer icon ko silently replace nahi kiya ja sakta. Ye option custom MANSI home-screen shortcut banata hai.", 12f).apply {
            setTextColor(Color.LTGRAY); setPadding(0, dp(14), 0, 0)
        })
        scroll.addView(content)
        root.addView(scroll)
        setContentView(root)
        renderPreview()
    }

    private fun actionButton(title: String, click: () -> Unit) = Button(this).apply {
        text = title
        isAllCaps = false
        setTextColor(Color.WHITE)
        background = GradientDrawable().apply {
            cornerRadius = dp(14).toFloat()
            setColor(Color.rgb(34, 31, 58))
            setStroke(dp(1), Color.rgb(92, 78, 150))
        }
        setPadding(dp(12), dp(7), dp(12), dp(7))
        val lp = LinearLayout.LayoutParams(-1, dp(52))
        lp.bottomMargin = dp(9)
        layoutParams = lp
        setOnClickListener { click() }
    }

    private fun renderPreview() {
        previewBg.colors = intArrayOf(selectedA, selectedB)
        val bitmap = chosenBitmap
        if (bitmap != null) {
            preview.setImageBitmap(Bitmap.createScaledBitmap(bitmap, 512, 512, true))
        } else {
            preview.setImageResource(android.R.drawable.sym_def_app_icon)
            preview.imageTintList = null
        }
    }

    private fun iconBitmap(): Bitmap {
        val size = 512
        val out = Bitmap.createBitmap(size, size, Bitmap.Config.ARGB_8888)
        val canvas = Canvas(out)
        val paint = Paint(Paint.ANTI_ALIAS_FLAG)
        paint.shader = LinearGradient(0f, 0f, size.toFloat(), size.toFloat(), selectedA, selectedB, Shader.TileMode.CLAMP)
        canvas.drawRoundRect(0f, 0f, size.toFloat(), size.toFloat(), 110f, 110f, paint)
        paint.shader = null
        val source = chosenBitmap
        if (source != null) {
            val side = minOf(source.width, source.height)
            val crop = Bitmap.createBitmap(source, (source.width-side)/2, (source.height-side)/2, side, side)
            val scaled = Bitmap.createScaledBitmap(crop, 330, 330, true)
            val path = Path().apply { addRoundRect(91f, 91f, 421f, 421f, 76f, 76f, Path.Direction.CW) }
            canvas.save(); canvas.clipPath(path)
            canvas.drawBitmap(scaled, 91f, 91f, Paint(Paint.ANTI_ALIAS_FLAG))
            canvas.restore()
        } else {
            paint.color = Color.WHITE
            paint.textAlign = Paint.Align.CENTER
            paint.textSize = 250f
            canvas.drawText("M", 256f, 340f, paint)
        }
        return out
    }

    private fun savePng() {
        try {
            val values = android.content.ContentValues().apply {
                put(MediaStore.Images.Media.DISPLAY_NAME, "MANSI-Custom-Icon.png")
                put(MediaStore.Images.Media.MIME_TYPE, "image/png")
                if (Build.VERSION.SDK_INT >= 29) put(MediaStore.Images.Media.RELATIVE_PATH, "Pictures/MANSI Icons")
            }
            val uri = contentResolver.insert(MediaStore.Images.Media.EXTERNAL_CONTENT_URI, values)
            if (uri == null) throw IllegalStateException("Could not create file")
            contentResolver.openOutputStream(uri)?.use { iconBitmap().compress(Bitmap.CompressFormat.PNG, 100, it) }
            Toast.makeText(this, "Icon Pictures/MANSI Icons mein save ho gaya 💖", Toast.LENGTH_LONG).show()
        } catch (e: Exception) {
            Toast.makeText(this, "Save failed: ${e.message}", Toast.LENGTH_LONG).show()
        }
    }

    private fun pinCustomShortcut() {
        if (Build.VERSION.SDK_INT < 26) {
            Toast.makeText(this, "Custom home shortcut ke liye Android 8+ chahiye", Toast.LENGTH_LONG).show()
            return
        }
        val manager = getSystemService(ShortcutManager::class.java)
        if (!manager.isRequestPinShortcutSupported) {
            Toast.makeText(this, "Launcher pinned shortcuts support nahi karta", Toast.LENGTH_LONG).show()
            return
        }
        val launch = packageManager.getLaunchIntentForPackage(packageName) ?: Intent(this, javaClass)
        val shortcut = ShortcutInfo.Builder(this, "mansi-custom-home-icon")
            .setShortLabel("MANSI AI")
            .setLongLabel("MANSI AI — Custom Icon")
            .setIcon(Icon.createWithBitmap(iconBitmap()))
            .setIntent(launch)
            .build()
        manager.requestPinShortcut(shortcut, null)
        Toast.makeText(this, "Home screen par shortcut add karne ki request bhej di ✨", Toast.LENGTH_LONG).show()
    }
}
