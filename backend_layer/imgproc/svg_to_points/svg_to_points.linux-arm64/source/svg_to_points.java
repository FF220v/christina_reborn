import processing.core.*; 
import processing.data.*; 
import processing.event.*; 
import processing.opengl.*; 

import geomerative.*; 

import java.util.HashMap; 
import java.util.ArrayList; 
import java.io.File; 
import java.io.BufferedReader; 
import java.io.PrintWriter; 
import java.io.InputStream; 
import java.io.OutputStream; 
import java.io.IOException; 

public class svg_to_points extends PApplet {



JSONObject settings;
JSONObject packed_result;
JSONArray packed_curves;
RShape grp;
RPoint[][] points;
boolean ignoringStyles = false;

public void setup(){
  settings = loadJSONObject("settings.json");
  float area_width =  settings.getInt("max_width");
  float area_height = settings.getInt("max_height");
  float angle_tolerance = settings.getFloat("angle_tolerance");
  float center_x = width/2;
  float center_y = height/2;
  RG.init(this);
  RG.ignoreStyles(ignoringStyles); 
  RG.setPolygonizerAngle(angle_tolerance);
  RG.setPolygonizer(RG.ADAPTATIVE);
  println("loading svg..."); 
  grp = RG.loadShape("file_to_convert.svg");
  println("loading complete");
  println("resizing and moving...");
  float orig_height = grp.getHeight();
  float orig_width = grp.getWidth();
  float orig_ratio = orig_width/orig_height;
  float area_ratio = area_width/area_height;
  float scale_factor;
  grp.translate(new RPoint(-grp.getX(), -grp.getY()));
  if(orig_ratio > area_ratio){
    scale_factor = area_width/orig_width;
    grp.scale(scale_factor);
    grp.translate(new RPoint(0,area_height/2-grp.getHeight()/2));
  }
  else{
    scale_factor = area_height/orig_height;
    grp.scale(scale_factor);
    grp.translate(new RPoint(area_width/2-grp.getWidth()/2,0));
  }
  print("scale factor: ");
  println(scale_factor);
  println("Getting points...");
  points = grp.getPointsInPaths(); 
  print("Amount of contours: ");
  println(points.length);
  println("Saving results");
  packed_result = settings;
  JSONArray all_curves;
  all_curves = new JSONArray();
  for(int i = 0; i<points.length; i++){
    JSONArray curve;
    curve = new JSONArray();
    for(int j = 0;j<points[i].length;j++){
      JSONArray p;
      p = new JSONArray();
      p.setInt(0,PApplet.parseInt(points[i][j].x*10000));
      p.setInt(1,PApplet.parseInt(points[i][j].y*10000)); 
      curve.setJSONArray(j,p);
    }
    all_curves.setJSONArray(i,curve);
  }
  packed_result.setJSONArray("data", all_curves);
  packed_result.setString("units", "10^-7 meters");
  saveJSONObject(packed_result, "data/result.json", "compact");
  println("results saved");
  exit();
}

/*
void draw(){
  for(int i = 0; i<points.length; i++){
  if (points[i] != null) {
      beginShape();
      for(int j = 0; j<points[i].length; j++){
        vertex(points[i][j].x, points[i][j].y);
      }
      endShape();
    }
  }
}
*/
  static public void main(String[] passedArgs) {
    String[] appletArgs = new String[] { "svg_to_points" };
    if (passedArgs != null) {
      PApplet.main(concat(appletArgs, passedArgs));
    } else {
      PApplet.main(appletArgs);
    }
  }
}
