package com.abhisek.activitysensor;

import android.content.Intent;
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
import android.widget.Button;
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

    Button btn_stop ;

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

        btn_stop = (Button) findViewById(R.id.button_stop);

        btn_stop.setOnClickListener(new View.OnClickListener() {

            @Override
            public void onClick(View v) {

                String mode = "Select";

                Intent intent = new Intent(getApplicationContext(), StartActivity.class);
                intent.putExtra("mode",mode);
                startActivity(intent);

                finish();


            }
        });

        sensorManager = (SensorManager) getSystemService(SENSOR_SERVICE);
        lastUpdate = System.currentTimeMillis();


        if (sensorManager.getDefaultSensor(Sensor.TYPE_ACCELEROMETER) == null) {
            // fail ! we dont have an accelerometer!
            Toast.makeText(this, "This device don't have an accelerometer sensor !", Toast.LENGTH_SHORT)
                    .show();
        }


    }

    @Override
    public void onSensorChanged(SensorEvent event) {

        //getting the travelling mode data from Start Activity
        Bundle extras = getIntent().getExtras();
        String mode = extras.getString("mode");
//        Toast.makeText(this, mode, Toast.LENGTH_SHORT).show();

        if (event.sensor.getType() == Sensor.TYPE_ACCELEROMETER) {
            getAccelerometer(event,mode);
//            SystemClock.sleep(10);
        }

    }

    /**
     * Getting accelerometer data
     * @param event
     */
    private void getAccelerometer(SensorEvent event, String mode) {
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

            String date = new SimpleDateFormat("yyyy-MM-dd").format(new Date());

            date= date.replace("-","");

            String fileName = "AccSensor_Data_"+date+".csv";

            write2csv(values, timestamp, mode, fileName);

            if (color) {
                view.setBackgroundColor(Color.GREEN);
            } else {
                view.setBackgroundColor(Color.RED);
            }
            color = !color;
        }
    }

    /**
     * write to csv file
     * @param values
     * @param timestamp
     * @param mode
     * @param fileName
     */
    private void write2csv(float[] values, String timestamp, String mode, String fileName) {

        try {

            //adding runtime permission for writing data to storage
            if(shouldAskPermission()) {
                String[] perms = {"android.permission.WRITE_EXTERNAL_STORAGE"};
                int permsRequestCode = 200;
                requestPermissions(perms, permsRequestCode);
            }

            String baseDir = android.os.Environment.getExternalStorageDirectory().getAbsolutePath();
            String filePath = baseDir + File.separator + fileName;
            File f = new File(filePath);
            CSVWriter writer;

            // File exist
            if (f.exists() && !f.isDirectory()) {
                FileWriter mFileWriter = new FileWriter(filePath, true); // true is for append mode
                writer = new CSVWriter(mFileWriter);
            } else {
                writer = new CSVWriter(new FileWriter(filePath));
                String[] data = {"x-value", "y-value", "z-value", "timestamp","travel-mode"};
                writer.writeNext(data);
            }

            String[] data = {String.valueOf(values[0]), String.valueOf(values[1]), String.valueOf(values[2]), timestamp, mode};
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
        // register this class as a listener for the orientation and accelerometer sensors
        sensorManager.registerListener(this,
                sensorManager.getDefaultSensor(Sensor.TYPE_ACCELEROMETER),
                SensorManager.SENSOR_DELAY_NORMAL);
        Toast.makeText(this, "Activity sensor running...", Toast.LENGTH_SHORT)
                .show();
    }

    @Override
    protected void onPause() {
        // unregister listener
        super.onPause();
//        sensorManager.unregisterListener(this);
//        Toast.makeText(this, "App paused ...", Toast.LENGTH_SHORT)
//                .show();
    }

    /**
     * Adding permission
     * @return
     */
    private boolean shouldAskPermission(){

        return(Build.VERSION.SDK_INT>Build.VERSION_CODES.LOLLIPOP_MR1);

    }

    /**
     * Not used
     * @param lat1
     * @param lon1
     * @param lat2
     * @param lon2
     * @return
     */
    public double getDistance(double lat1, double lon1, double lat2, double lon2)
    {
        double latA = Math.toRadians(lat1);
        double lonA = Math.toRadians(lon1);
        double latB = Math.toRadians(lat2);
        double lonB = Math.toRadians(lon2);
        double cosAng = (Math.cos(latA) * Math.cos(latB) * Math.cos(lonB-lonA)) +
                (Math.sin(latA) * Math.sin(latB));
        double ang = Math.acos(cosAng);
        double dist = ang *6371;
        return dist;
    }


}
