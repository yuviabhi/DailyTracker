package com.abhisek.activitysensor;

import android.app.ProgressDialog;
import android.content.Intent;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.Toast;

import java.io.DataOutputStream;
import java.io.File;
import java.io.FileInputStream;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;
import java.util.Random;

public class FileUploadActivity extends AppCompatActivity {


    final String uploadFileName_dayT = MainActivity.getFileName();
    final String uploadFileName_nday = "AccSensor_Data_merged.csv";
    Button btn_upload_nday = null;
    Button btn_upload_dayT = null;
    Button btn_track = null;
    boolean is_uploaded_nday = false;
    boolean is_uploaded_dayT = false;
    int serverResponseCode = 0;
    ProgressDialog dialog = null;
    /*************
     * Php script path
     ****************/
    String upLoadServerUri = "http://192.168.43.207/activity_sensor/UploadToServer.php";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_file_upload);

        btn_upload_nday = (Button) findViewById(R.id.button_nDay);

        btn_upload_dayT = (Button) findViewById(R.id.button_dayT);

        btn_track = (Button) findViewById(R.id.button_trackToday);


        btn_upload_nday.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {

                dialog = ProgressDialog.show(FileUploadActivity.this, "", "Uploading file...", true);

                new Thread(new Runnable() {
                    public void run() {
                        runOnUiThread(new Runnable() {
                            public void run() {
                                //messageText.setText("uploading started.....");
                                Toast.makeText(getApplicationContext(), "Uploading...", Toast.LENGTH_SHORT).show();
                            }
                        });

                        String baseDir = android.os.Environment.getExternalStorageDirectory().getAbsolutePath();
                        String uploadFilePath = baseDir + File.separator + uploadFileName_nday;

                        int server_response_code = uploadFile(uploadFilePath);
                        if (server_response_code == 200) {
                            is_uploaded_nday = true;
                        }

                    }

                }).start();
            }
        });


        btn_upload_dayT.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {

                dialog = ProgressDialog.show(FileUploadActivity.this, "", "Uploading file...", true);

                new Thread(new Runnable() {
                    public void run() {
                        runOnUiThread(new Runnable() {
                            public void run() {
                                //messageText.setText("uploading started.....");
                                Toast.makeText(getApplicationContext(), "Uploading...", Toast.LENGTH_SHORT).show();
                            }
                        });

                        String baseDir = android.os.Environment.getExternalStorageDirectory().getAbsolutePath();
                        String uploadFilePath = baseDir + File.separator + uploadFileName_dayT;
                        int server_response_code = uploadFile(uploadFilePath);
                        if (server_response_code == 200) {
                            is_uploaded_dayT = true;
                        }

                    }

                }).start();
            }
        });


        btn_track.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {

                dialog = ProgressDialog.show(FileUploadActivity.this, "", "Tracking your day...", true);

                new Thread(new Runnable() {
                    public void run() {
                        runOnUiThread(new Runnable() {
                            public void run() {
                                //messageText.setText("uploading started.....");
                                Toast.makeText(getApplicationContext(), "Computing...", Toast.LENGTH_SHORT).show();
                            }
                        });


                        if (is_uploaded_dayT && is_uploaded_nday) {

                            boolean is_regular_day = track_your_day();
                            dialog.dismiss();
                            if (is_regular_day) {
                                Intent intent = new Intent(getApplicationContext(), RegularActivity.class);
                                //                intent.putExtra("mode",mode);
                                startActivity(intent);
                            } else {

                                Intent intent = new Intent(getApplicationContext(), IrregularActivity.class);
                                //                intent.putExtra("mode",mode);
                                startActivity(intent);

                            }
                        } else {
                            Toast.makeText(FileUploadActivity.this, "Please upload files !", Toast.LENGTH_SHORT).show();
                        }


                    }

                }).start();
            }
        });

    }

    private boolean track_your_day() {


//        int random=1;

        int random_num = getRandom(0, 100);

        int sleep_timer = getRandom(5, 10);

        try {
            Thread.sleep(sleep_timer * 1000);  //1000 = 1 sec
        } catch (InterruptedException e) {
            e.printStackTrace();
        }

        return random_num % 2 == 0;
    }

    private int getRandom(int Low, int High) {

        Random r = new Random();
//        int Low = 1;
//        int High = 100;
        int Result = r.nextInt(High - Low) + Low;
        return Result;
    }


    private int uploadFile(String sourceFileUri) {

        String fileName = sourceFileUri;

        HttpURLConnection conn = null;
        DataOutputStream dos = null;
        String lineEnd = "\r\n";
        String twoHyphens = "--";
        String boundary = "*****";
        int bytesRead, bytesAvailable, bufferSize;
        byte[] buffer;
        int maxBufferSize = 1 * 1024 * 1024;
        File sourceFile = new File(sourceFileUri);

        if (!sourceFile.isFile()) {

            dialog.dismiss();

            Log.e("uploadFile", "Source File not exist :"
                    + uploadFileName_dayT);

            runOnUiThread(new Runnable() {
                public void run() {
                    //messageText.setText("Source File not exist :"
                    //        +uploadFilePath + "" + uploadFileName_dayT);
                    Toast.makeText(FileUploadActivity.this, "Source File not Exist", Toast.LENGTH_SHORT).show();
                }
            });

            return 0;

        } else {
            try {

                // open a URL connection to the Servlet
                FileInputStream fileInputStream = new FileInputStream(sourceFile);
                URL url = new URL(upLoadServerUri);

                // Open a HTTP  connection to  the URL
                conn = (HttpURLConnection) url.openConnection();
                conn.setDoInput(true); // Allow Inputs
                conn.setDoOutput(true); // Allow Outputs
                conn.setUseCaches(false); // Don't use a Cached Copy
                conn.setRequestMethod("POST");
                conn.setRequestProperty("Connection", "Keep-Alive");
                conn.setRequestProperty("ENCTYPE", "multipart/form-data");
                conn.setRequestProperty("Content-Type", "multipart/form-data;boundary=" + boundary);
                conn.setRequestProperty("uploaded_file", fileName);

                dos = new DataOutputStream(conn.getOutputStream());

                dos.writeBytes(twoHyphens + boundary + lineEnd);
                dos.writeBytes("Content-Disposition: form-data; name='uploaded_file';filename='"
                        + fileName + "'" + lineEnd);

                dos.writeBytes(lineEnd);

                // create a buffer of  maximum size
                bytesAvailable = fileInputStream.available();

                bufferSize = Math.min(bytesAvailable, maxBufferSize);
                buffer = new byte[bufferSize];

                // read file and write it into form...
                bytesRead = fileInputStream.read(buffer, 0, bufferSize);

                while (bytesRead > 0) {

                    dos.write(buffer, 0, bufferSize);
                    bytesAvailable = fileInputStream.available();
                    bufferSize = Math.min(bytesAvailable, maxBufferSize);
                    bytesRead = fileInputStream.read(buffer, 0, bufferSize);

                }

                // send multipart form data necesssary after file data...
                dos.writeBytes(lineEnd);
                dos.writeBytes(twoHyphens + boundary + twoHyphens + lineEnd);

                // Responses from the server (code and message)
                serverResponseCode = conn.getResponseCode();
                String serverResponseMessage = conn.getResponseMessage();

                Log.i("uploadFile", "HTTP Response is : "
                        + serverResponseMessage + ": " + serverResponseCode);

                if (serverResponseCode == 200) {

                    runOnUiThread(new Runnable() {
                        public void run() {

//                            String msg = "File Upload Completed.\n\n See uploaded file here : \n\n"
//                                    +" http://www.androidexample.com/media/uploads/"
//                                    +uploadFileName_dayT;

                            //messageText.setText(msg);
                            Toast.makeText(FileUploadActivity.this, "File Upload Successful.",
                                    Toast.LENGTH_SHORT).show();
                        }
                    });
                }

                //close the streams //
                fileInputStream.close();
                dos.flush();
                dos.close();

            } catch (MalformedURLException ex) {

                dialog.dismiss();
                ex.printStackTrace();

                runOnUiThread(new Runnable() {
                    public void run() {
                        //messageText.setText("MalformedURLException Exception : check script url.");
                        Toast.makeText(FileUploadActivity.this, "MalformedURLException",
                                Toast.LENGTH_SHORT).show();
                    }
                });

                Log.e("Upload file to server", "error: " + ex.getMessage(), ex);
            } catch (Exception e) {

                dialog.dismiss();
                e.printStackTrace();

                runOnUiThread(new Runnable() {
                    public void run() {
                        //messageText.setText("Got Exception : see logcat ");
                        Toast.makeText(FileUploadActivity.this, "Got Connection Exception : see logcat ",
                                Toast.LENGTH_SHORT).show();
                    }
                });
                Log.e("Upload file to server Exception", "Exception : "
                        + e.getMessage(), e);
            }
            dialog.dismiss();
            return serverResponseCode;

        } // End else block
    }


}
