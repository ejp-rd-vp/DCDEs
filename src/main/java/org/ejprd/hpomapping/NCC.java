package org.ejprd.hpomapping;

import javax.net.ssl.HttpsURLConnection;
import javax.net.ssl.SSLContext;
import javax.net.ssl.TrustManager;
import javax.net.ssl.X509TrustManager;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.Reader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.nio.charset.StandardCharsets;

public class NCC {

    public static String getHPOterms(String line, int sleepMillisec) throws Exception
    {
        // dirty hacking around expired certificate
        TrustManager[] trustAllCerts = new TrustManager[]{
                new X509TrustManager() {
                    public java.security.cert.X509Certificate[] getAcceptedIssuers() {return null;}
                    public void checkClientTrusted(java.security.cert.X509Certificate[] certs, String authType){}
                    public void checkServerTrusted(java.security.cert.X509Certificate[] certs, String authType){}
                }
        };
        SSLContext sc = SSLContext.getInstance("SSL");
        sc.init(null, trustAllCerts, new java.security.SecureRandom());
        HttpsURLConnection.setDefaultSSLSocketFactory(sc.getSocketFactory());

        String urlParameters  = "{\"text\":\""+line+"\"}";
        byte[] postData       = urlParameters.getBytes( StandardCharsets.UTF_8 );
        int    postDataLength = postData.length;
        String request        = "https://ncr.ccm.sickkids.ca/curr/annotate/";
        URL url            = new URL( request );
        HttpURLConnection conn= (HttpURLConnection) url.openConnection();
        conn.setDoOutput( true );
        conn.setInstanceFollowRedirects( false );
        conn.setRequestMethod( "POST" );
        conn.setRequestProperty( "Content-Type", "application/json");
        conn.setRequestProperty( "charset", "utf-8");
        conn.setRequestProperty( "Content-Length", Integer.toString( postDataLength ));
        conn.setUseCaches( false );

        try { conn.getOutputStream().write(postData); }catch(java.net.ConnectException e)
        {
            System.out.println(e);
            System.out.println("attempt 2:");
            try { conn.getOutputStream().write(postData); }catch(java.net.ConnectException e2)
            {
                System.out.println(e);
                System.out.println("attempt 3:");
                try { conn.getOutputStream().write(postData); }catch(java.net.ConnectException e3)
                {
                    System.out.println(e);
                    System.out.println("3rd attempt fail, quitting!!!");
                    System.exit(1);
                }
            }
        }

        Reader in = new BufferedReader(new InputStreamReader(conn.getInputStream(), "UTF-8"));
        StringBuilder sb = new StringBuilder();
        for (int c; (c = in.read()) >= 0;)
            sb.append((char)c);
        String response = sb.toString();

        Thread.sleep(sleepMillisec);

        return response;
    }

}
