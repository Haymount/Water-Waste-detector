package com.example.vandmler2000;
import androidx.appcompat.app.AppCompatActivity;
import android.annotation.SuppressLint;
import android.app.Activity;
import android.os.Bundle;
import android.view.KeyEvent;
import android.webkit.ClientCertRequest;
import android.webkit.WebResourceRequest;
import android.webkit.WebView;
import android.webkit.WebViewClient;

public class MainActivity extends AppCompatActivity {

    private WebView webView;

    @SuppressLint("SetJavaScriptEnabled")
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        webView = findViewById(R.id.webWiew);
        
        webView.getSettings().setJavaScriptEnabled(true);
        webView.loadUrl("http://192.168.1.221:8000"); //Her fortæller vi hvilken hjemmeside den skal bruge
    }
    
    @Override //Her lave vi tilbage knappen, så man kan bruge den i appen
    public boolean onKeyDown(int keyCode, KeyEvent event){
        if(keyCode == KeyEvent.KEYCODE_BACK && this.webView.canGoBack()) {
            this.webView.goBack();
            return true;
        }
        return super.onKeyDown(keyCode, event);
    }
}

class CustomWebViewClient extends WebViewClient{
    private Activity activity;

    public CustomWebViewClient(Activity activity){
        this.activity = activity;
    }
    //når API er undre 24
    @Override
    public boolean shouldOverrideUrlLoading(WebView webView, String url){
        return false;
    }
    //når API er 24 eller over
    @Override
    public boolean shouldOverrideUrlLoading(WebView webView, WebResourceRequest request){
        return false;
    }

}