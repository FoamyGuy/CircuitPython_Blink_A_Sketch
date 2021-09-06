
color([1,1,1]){
difference(){
    cylinder(r=20/2, h=12, $fn=45);
    
    translate([0,0,4])
    cylinder(r=6.1/2, h=12, $fn=45);
}

translate([4.6,0,8/2 + 4])
cube([5,5,8], center=true);
}