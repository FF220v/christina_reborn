import geomerative.*;

JSONObject settings;
JSONObject packed_result;
JSONArray packed_curves;
RShape grp;
RPoint[][] points;
boolean ignoringStyles = false;


void setup(){
  println("loading settings..."); 
  surface.setVisible(false);
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
  println("getting points...");
  points = grp.getPointsInPaths(); 
  print("amount of contours: ");
  println(points.length);
  print("amount of points: ");
  int num_of_points = calculate_num_of_points();
  println(num_of_points);
  println("saving results...");
  packed_result = settings;
  JSONArray all_curves;
  all_curves = new JSONArray();
  for(int i = 0; i<points.length; i++){
    JSONArray curve;
    curve = new JSONArray();
    for(int j = 0;j<points[i].length;j++){
      JSONArray p;
      p = new JSONArray();
      p.setInt(0,int(points[i][j].x*10000));
      p.setInt(1,int(points[i][j].y*10000)); 
      curve.setJSONArray(j,p);
    }
    all_curves.setJSONArray(i,curve);
  }
  packed_result.setJSONArray("data", all_curves);
  packed_result.setString("units", "10^-7 meters");
  packed_result.setInt("num_of_contours", points.length);
  packed_result.setInt("num_of_points", num_of_points);
  saveJSONObject(packed_result, "data/result.json", "compact");
  println("results saved");
  exit();
}

int calculate_num_of_points(){
  int counter=0;
  for(int i = 0; i<points.length; i++){
    for(int j = 0; j<points[i].length; j++){
      counter++;  
    }  
  }
  return counter;
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
