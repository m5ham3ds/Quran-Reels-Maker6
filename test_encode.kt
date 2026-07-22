import android.net.Uri

fun main() {
    val url = "https://qalam249-whisperx-frontend.hf.space/gradio_api/file=/tmp/gradio/9bc9/1783_Surat Fatir ｜ Nasser #quran.wav"
    println(url.replace(" ", "%20").replace("#", "%23"))
    // We don't have android.net.Uri in pure kotlin script easily, so we can use java.net.URLEncoder
}
