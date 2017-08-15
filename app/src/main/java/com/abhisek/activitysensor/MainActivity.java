package com.abhisek.activitysensor;

import android.graphics.Color;
import android.hardware.Sensor;
import android.hardware.SensorEvent;
import android.hardware.SensorEventListener;
import android.hardware.SensorManager;
import android.os.Build;
import android.os.Bundle;
import android.os.SystemClock;
import android.support.v7.app.AppCompatActivity;
import android.view.View;
import android.view.Window;
import android.view.WindowManager;
import android.widget.TextView;
import android.widget.Toast;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.text.DateFormat;
import java.text.SimpleDateFormat;
import java.util.Date;

import au.com.bytecode.opencsv.CSVWriter;

public class MainActivity extends AppCompatActivity implements SensorEventListener {

    private SensorManager sensorManager;
    private boolean color = false;
    private View view;
    private long lastUpdate;


    private TextView txtView_x;
    private TextView txtView_y;
    private TextView txtView_z;
    private TextView txtView_time;

    /**
     * Called when the activity is first created.
     */
    @Override
    public void onCreate(Bundle savedInstanceState) {
        requestWindowFeature(Window.FEATURE_NO_TITLE);
        getWindow().setFlags(WindowManager.LayoutParams.FLAG_FULLSCREEN,
                WindowManager.LayoutParams.FLAG_FULLSCREEN);

        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        view = findViewById(R.id.textView);
        view.setBackgroundColor(Color.GREEN);

        txtView_x = (TextView) findViewById(R.id.textView_x);
        txtView_y = (TextView) findViewById(R.id.textView_y);
        txtView_z = (TextView) findViewById(R.id.textView_z);
        txtView_time = (TextView) findViewById(R.id.textView_time);


        sensorManager = (SensorManager) getSystemService(SENSOR_SERVICE);
        lastUpdate = System.currentTimeMillis();


        if (sensorManager.getDefaultSensor(Sensor.TYPE_ACCELEROMETER) == null) {
            // fai! we dont have an accelerometer!
            Toast.makeText(this, "This device don't have an accelerometer!", Toast.LENGTH_SHORT)
                    .show();
        }
    }

    @Override
    public void onSensorChanged(SensorEvent event) {
        if (event.sensor.getType() == Sensor.TYPE_ACCELEROMETER) {
            getAccelerometer(event);
        }

    }

    private void getAccelerometer(SensorEvent event) {
        float[] values = event.values;
        // Movement
        float x = values[0];
        float y = values[1];
        float z = values[2];

        float accelationSquareRoot = (x * x + y * y + z * z)
                / (SensorManager.GRAVITY_EARTH * SensorManager.GRAVITY_EARTH);
        long actualTime = event.timestamp;
//        System.out.println("accelationSquareRoot : " + accelationSquareRoot);
        if (accelationSquareRoot >= 2) //
        {
            if (actualTime - lastUpdate < 200) {
                return;
            }
            lastUpdate = actualTime;
            Toast.makeText(this, "Device was shaked !", Toast.LENGTH_SHORT).show();
            txtView_x.setText("X value : " + String.valueOf(x));
            txtView_y.setText("Y value : " + String.valueOf(y));
            txtView_z.setText("Z value : " + String.valueOf(z));
            SimpleDateFormat simpleDateFormat = new SimpleDateFormat("dd-MM-yyyy HH:mm:ss");
//            Date resultdate = new Date(actualTime);
//            System.out.println(simpleDateFormat.format(resultdate));
//            String timestamp = simpleDateFormat.format(actualTime / 1000000L);

//            long elapsedRealtime = SystemClock.elapsedRealtime();
//            long mUptimeMillis = (System.currentTimeMillis() - elapsedRealtime);
//            long timeInMillis = ((mUptimeMillis + (actualTime - System.nanoTime())) / 1000000L);
//            long timeInMillis =  (actualTime - System.nanoTime()) / 1000000L;
//            String timestamp = simpleDateFormat.format(timeInMillis);
//            txtView_time.setText("Timestamp : " + timestamp);
//            System.out.println("Timestamp : " + timestamp + "   actualTime : " + actualTime + "    timeInMillis " + timeInMillis + "    (new Date()).getTime()" + (new Date()).getTime());

            String timestamp = simpleDateFormat.format((new Date()).getTime());
            txtView_time.setText("Timestamp : " + timestamp);
//            System.out.println("Timestamp : " + timestamp);

            write2csv(values, timestamp);

            if (color) {
                view.setBackgroundColor(Color.GREEN);
            } else {
                view.setBackgroundColor(Color.RED);
            }
            color = !color;
        }
    }

    private void write2csv(float[] values, String timestamp) {

        try {

            //adding runtime permission for writing data to storage
            if(shouldAskPermission()) {
                String[] perms = {"android.permission.WRITE_EXTERNAL_STORAGE"};
                int permsRequestCode = 200;
                requestPermissions(perms, permsRequestCode);
            }

            String baseDir = android.os.Environment.getExternalStorageDirectory().getAbsolutePath();
            String fileName = "AccelerometerSensorData.csv";
            String filePath = baseDir + File.separator + fileName;
            File f = new File(filePath);
            CSVWriter writer;
            // File exist
            if (f.exists() && !f.isDirectory()) {
                FileWriter mFileWriter = new FileWriter(filePath, true); // true is for append mode
                writer = new CSVWriter(mFileWriter);
            } else {
                writer = new CSVWriter(new FileWriter(filePath));
                String[] data = {"x-value", "y-value", "z-value", "timestamp"};
                writer.writeNext(data);
            }

            String[] data = {String.valueOf(values[0]), String.valueOf(values[1]), String.valueOf(values[2]), timestamp};
            writer.writeNext(data);
            writer.close();

        } catch (IOException e) {
            e.printStackTrace();
            System.out.println(e.toString());
        }
    }

    @Override
    public void onAccuracyChanged(Sensor sensor, int accuracy) {

    }

    @Override
    protected void onResume() {
        super.onResume();
        // register this class as a listener for the orientation and
        // accelerometer sensors
        sensorManager.registerListener(this,
                sensorManager.getDefaultSensor(Sensor.TYPE_ACCELEROMETER),
                SensorManager.SENSOR_DELAY_NORMAL);
        Toast.makeText(this, "App resumed ...", Toast.LENGTH_SHORT)
                .show();
    }

    @Override
    protected void onPause() {
        // unregister listener
        super.onPause();
        sensorManager.unregisterListener(this);
        Toast.makeText(this, "App paused ...", Toast.LENGTH_SHORT)
                .show();
    }

    private boolean shouldAskPermission(){

        return(Build.VERSION.SDK_INT>Build.VERSION_CODES.LOLLIPOP_MR1);

    }
}
