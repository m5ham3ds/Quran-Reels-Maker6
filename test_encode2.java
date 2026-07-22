import java.net.URLEncoder;

public class test_encode2 {
    public static void main(String[] args) throws Exception {
        String url = "https://host.com/gradio_api/file=/tmp/gradio/9bc9/1783_Surat Fatir ｜ Nasser #quran.wav";
        String prefix = "file=";
        int fileIdx = url.indexOf(prefix);
        if (fileIdx != -1) {
            String baseUrl = url.substring(0, fileIdx + prefix.length());
            String pathStr = url.substring(fileIdx + prefix.length());
            String[] segments = pathStr.split("/");
            StringBuilder encodedPath = new StringBuilder();
            for (int i = 0; i < segments.length; i++) {
                if (i > 0) encodedPath.append("/");
                encodedPath.append(URLEncoder.encode(segments[i], "UTF-8").replace("+", "%20"));
            }
            System.out.println(baseUrl + encodedPath.toString());
        }
    }
}
