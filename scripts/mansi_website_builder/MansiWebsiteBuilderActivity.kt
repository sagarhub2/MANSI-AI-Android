package com.jarvis.assistant.ui.tools

import android.content.Intent
import android.net.Uri
import android.os.Bundle
import android.webkit.JavascriptInterface
import android.webkit.WebChromeClient
import android.webkit.WebResourceRequest
import android.webkit.WebView
import android.webkit.WebViewClient
import android.widget.Toast
import androidx.activity.result.contract.ActivityResultContracts
import androidx.appcompat.app.AppCompatActivity
import com.jarvis.assistant.R
import java.io.OutputStreamWriter

class MansiWebsiteBuilderActivity : AppCompatActivity() {
    private lateinit var webView: WebView
    private var pendingHtml: String = ""
    private var pendingFilename: String = "mansi-website.html"

    private val saveDocument = registerForActivityResult(ActivityResultContracts.CreateDocument("text/html")) { uri: Uri? ->
        if (uri == null) {
            notifyPage("Save cancelled")
            return@registerForActivityResult
        }
        try {
            contentResolver.openOutputStream(uri)?.use { stream ->
                OutputStreamWriter(stream, Charsets.UTF_8).use { it.write(pendingHtml) }
            } ?: error("Could not open destination")
            Toast.makeText(this, "Website HTML saved successfully", Toast.LENGTH_LONG).show()
            notifyPage("Website saved successfully")
        } catch (error: Exception) {
            Toast.makeText(this, "Could not save: ${error.message}", Toast.LENGTH_LONG).show()
            notifyPage("Save failed")
        }
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_mansi_website_builder)
        webView = findViewById(R.id.websiteBuilderWebView)
        webView.settings.javaScriptEnabled = true
        webView.settings.domStorageEnabled = false
        webView.settings.allowFileAccess = true
        webView.settings.allowContentAccess = false
        webView.settings.javaScriptCanOpenWindowsAutomatically = false
        webView.webChromeClient = WebChromeClient()
        webView.webViewClient = object : WebViewClient() {
            override fun shouldOverrideUrlLoading(view: WebView?, request: WebResourceRequest?): Boolean {
                val url = request?.url?.toString() ?: return true
                return !url.startsWith("file:///android_asset/mansi-website-builder.html") &&
                    !url.startsWith("about:blank")
            }
        }
        webView.addJavascriptInterface(BuilderBridge(), "MansiBuilder")
        webView.loadUrl("file:///android_asset/mansi-website-builder.html")
    }

    private fun notifyPage(message: String) {
        if (::webView.isInitialized) {
            val safe = org.json.JSONObject.quote(message)
            webView.post { webView.evaluateJavascript("window.onNativeSaveResult && window.onNativeSaveResult($safe)", null) }
        }
    }

    inner class BuilderBridge {
        @JavascriptInterface
        fun saveHtml(filename: String, html: String) {
            pendingFilename = filename.replace(Regex("[^A-Za-z0-9._-]"), "_").take(70).ifBlank { "mansi-website.html" }
            if (!pendingFilename.endsWith(".html", true)) pendingFilename += ".html"
            pendingHtml = html
            runOnUiThread { saveDocument.launch(pendingFilename) }
        }

        @JavascriptInterface
        fun closeBuilder() {
            runOnUiThread { finish() }
        }
    }

    override fun onDestroy() {
        if (::webView.isInitialized) {
            webView.removeJavascriptInterface("MansiBuilder")
            webView.stopLoading()
            webView.destroy()
        }
        super.onDestroy()
    }
}
