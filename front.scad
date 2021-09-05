
SCREEN_CUTOUT_Y = 48.5;
SCREEN_CUTOUT_X = 65;

ENCODER_SHAFT_CUTOUT = 6.2 + 1.7;

// from centers of mount cutouts
PYPORTAL_X = 83;
PYPORTAL_Y = 59;


CASE_X = PYPORTAL_X+13;

CASE_KNOBS_SPACE = 30;
CASE_Y = PYPORTAL_Y+10 + CASE_KNOBS_SPACE;



module pyportal(){
    import("pyportal_flat_center.stl");
    
    
    translate([-2,0.5,0.23])
    color([0,0,0])
    cube([SCREEN_CUTOUT_X, SCREEN_CUTOUT_Y, 0.5], center=true);
    
    
} 



module outter_shell(){
    
    difference(){
        difference(){
            minkowski(){
                cube([CASE_X, CASE_Y, 20], center=true);
                sphere(r=10, $fn=50);
            }
            
            // cut in half
            translate([0,0, 50/2]){
                cube([150, 150, 50], center=true);
            }
        }
        
        translate([0,0, 1.5]){
            difference(){
                minkowski(){
                    cube([CASE_X-4, CASE_Y-4, 20], center=true);
                    sphere(r=10, $fn=50);
                }
            }
        }
    }

}

module pyportal_mount_cutouts(){
    translate([83/2, 59/2, 0])
    cylinder(r=3.5/2, h=100, $fn=30, center=true);
    
    translate([-83/2, 59/2, 0])
    cylinder(r=3.5/2, h=100, $fn=30, center=true);
    
    translate([83/2, -59/2, 0])
    cylinder(r=3.5/2, h=100, $fn=30, center=true);
    
    translate([-83/2, -59/2, 0])
    cylinder(r=3.5/2, h=100, $fn=30, center=true);
}
difference(){
    color([1,0,0])
    outter_shell();
    translate([2,CASE_KNOBS_SPACE-17,0]){
        pyportal_mount_cutouts();
        
        // screen cutout
        translate([-2,0,-20])
        cube([SCREEN_CUTOUT_X, SCREEN_CUTOUT_Y, 20], center=true);
    
        
    }
    
    
    // encoder cutouts
    translate([34, -34,0 ])
    cylinder(r=ENCODER_SHAFT_CUTOUT/2, h=50, $fn=30, center=true);
    
    translate([-30, -34,0 ])
    cylinder(r=ENCODER_SHAFT_CUTOUT/2, h=50, $fn=30, center=true);
    
    
    // corner cutout
    //translate([60, -40, 0])
    //cube([50, 90, 60], center=true);
    
    // USB cable cutout
    translate([40,31,-11])
    cube([50, 14, 12], center=true);
}


// corner screw posts
translate([(CASE_X+4)/2,(CASE_Y+4)/2,-3])
difference(){
    union(){
        translate([0,0,-4])
        cylinder(r=5, h=14, center=true, $fn=40);
        translate([0,0,-10])
        sphere(r=5, $fn=40);
    }
    translate([0,0,-3.4])
    cylinder(r=2.5/2, h=13, center=true, $fn=30);
}

translate([-(CASE_X+4)/2,(CASE_Y+4)/2,-3])
difference(){
    union(){
        translate([0,0,-4])
        cylinder(r=5, h=14, center=true, $fn=40);
        translate([0,0,-10])
        sphere(r=5, $fn=40);
    }
    translate([0,0,-3.4])
    cylinder(r=2.5/2, h=13, center=true, $fn=30);
}

translate([(CASE_X+4)/2,-(CASE_Y+4)/2,-3])
difference(){
    union(){
        translate([0,0,-4])
        cylinder(r=5, h=14, center=true, $fn=40);
        translate([0,0,-10])
        sphere(r=5, $fn=40);
    }
    translate([0,0,-3.4])
    cylinder(r=2.5/2, h=13, center=true, $fn=30);
}

translate([-(CASE_X+4)/2,-(CASE_Y+4)/2,-3])
difference(){
    union(){
        translate([0,0,-4])
        cylinder(r=5, h=14, center=true, $fn=40);
        translate([0,0,-10])
        sphere(r=5, $fn=40);
    }
    translate([0,0,-3.4])
    cylinder(r=2.5/2, h=13, center=true, $fn=30);
}

color([1,1,1]){
translate([34, -34,-9 ])
rotate([0,180,90])
import("encoder.stl");

translate([-30, -34,-9 ])
rotate([0,180,90])
import("encoder.stl");
}

translate([2,CASE_KNOBS_SPACE-17,-18]){
    pyportal();
    
    
    /*translate([-2,0.5,-6])
    color([0,1,0])
    cube([SCREEN_CUTOUT_X, SCREEN_CUTOUT_Y, 10], center=true);
    */
    
    
    // positive of screw holes
    //pyportal_mount_cutouts();
}

// stemma wire room placeholder
//translate([-83/2 -4, 7, 0])
//cube([5, 10, 5], center=true);


//