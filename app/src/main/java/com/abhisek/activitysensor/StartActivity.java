package com.abhisek.activitysensor;

import android.content.Intent;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.view.View;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.Spinner;
import android.widget.Toast;

public class StartActivity extends AppCompatActivity {

    Button btn_upload;
    private String[] arraySpinner;
    private Button button_start;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_start);

        this.arraySpinner = new String[] {
               "Select", "Walk", "Run", "Work-out", "Cycling", "Biking", "Travel by bus/car" , "Travel by train" , "Dummy shake", "Something else"
        };

        final Spinner s = (Spinner) findViewById(R.id.spinner_mode);

        ArrayAdapter<String> adapter = new ArrayAdapter<>(this,
                android.R.layout.simple_spinner_item, arraySpinner);
        s.setAdapter(adapter);



        button_start = (Button) findViewById(R.id.button_start);

        button_start.setOnClickListener(new View.OnClickListener() {

            @Override
            public void onClick(View v) {

                String mode = s.getSelectedItem().toString().trim();

                if(mode !="Select") {
                    Intent intent = new Intent(getApplicationContext(), MainActivity.class);
                    intent.putExtra("mode",mode);
                    startActivity(intent);
                } else  {
                    Toast.makeText(getApplicationContext(),"Select your activity mode !",Toast.LENGTH_SHORT).show();
                }

            }
        });


        btn_upload = (Button) findViewById(R.id.button_upload_data);

        btn_upload.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intent = new Intent(getApplicationContext(), FileUploadActivity.class);
//                intent.putExtra("mode",mode);
                startActivity(intent);
            }
        });


    }

    @Override
    public void onBackPressed() {

        super.onBackPressed();
        finish();

    }
}
