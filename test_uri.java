import java.net.URI;
import java.net.URL;

public class test_uri {
    public static void main(String[] args) throws Exception {
        String urlStr = "https://host.com/gradio_api/file=/tmp/abc/Surat Fatir ｜ Nasser #quran.wav";
        URL urlObj = new URL(urlStr);
        URI uri = new URI(
            urlObj.getProtocol(),
            urlObj.getUserInfo(),
            urlObj.getHost(),
            urlObj.getPort(),
            urlObj.getPath(),
            urlObj.getQuery(),
            urlObj.getRef()
        );
        System.out.println(uri.toASCIIString());
    }
}
