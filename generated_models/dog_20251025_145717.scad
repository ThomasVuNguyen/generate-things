// Realistic Medium-Complexity 3D-Printable Dog
// Overall size ~70 mm long, 50 mm tall

module paw() {
    // Simple paw with toes
    union() {
        // Main paw pad
        translate([0,0,3]) sphere(d=10,$fn=20);
        // Toes
        for(a=[-25,0,25])
            translate([sin(a)*4,cos(a)*4,7])
                sphere(d=4,$fn=12);
    }
}

module leg(len=25) {
    // Cylindrical leg with paw
    union() {
        cylinder(h=len,d1=10,d2=8,$fn=20);
        translate([0,0,len]) paw();
    }
}

module tail() {
    // Curved tail
    rotate([0,90,0])
        rotate_extrude(angle=180,$fn=40)
            translate([25,0,0]) circle(d=[6,4],$fn=20);
}

// Body
union() {
    // Torso
    translate([0,0,20]) scale([1.5,1,1]) sphere(d=40,$fn=50);
    
    // Head
    translate([-35,0,40]) sphere(d=25,$fn=50);
    
    // Snout
    translate([-50,0,38]) scale([1.2,0.8,0.7]) sphere(d=15,$fn=30);
    
    // Ears
    for(side=[-1,1])
        translate([-30,side*15,50])
            rotate([0,side*20,0])
                scale([0.5,1,1.5])
                    sphere(d=12,$fn=20);
    
    // Legs
    translate([20,15,0]) leg();
    translate([20,-15,0]) leg();
    translate([-20,15,0]) leg();
    translate([-20,-15,0]) leg();
    
    // Tail
    translate([25,0,25]) rotate([0,0,30]) tail();
    
    // Eyes
    for(side=[-1,1])
        difference() {
            translate([-45,side*8,45]) sphere(d=5,$fn=20);
            translate([-47,side*8,46]) sphere(d=2,$fn=10);
        }
    
    // Nose
    translate([-55,0,38]) sphere(d=3,$fn=15);
}