// Generated OpenSCAD code for a banana
// This is an example of what the AI might generate

module banana() {
    // Main banana body (curved)
    color([1.0, 0.9, 0.2]) {
        union() {
            // Curved banana shape using multiple spheres
            for(i = [0:5:100]) {
                rotate([0, 0, i*0.3]) {
                    translate([0, 0, i*0.4]) {
                        scale([1, 1, 0.8]) {
                            sphere(r=8 - i*0.05, $fn=32);
                        }
                    }
                }
            }
        }
    }
    
    // Banana tip (darker)
    color([0.8, 0.7, 0.1]) {
        translate([0, 0, 40]) {
            sphere(r=3, $fn=16);
        }
    }
    
    // Stem end
    color([0.6, 0.5, 0.1]) {
        translate([0, 0, -2]) {
            cylinder(h=4, r=6, $fn=16);
        }
    }
    
    // Surface ridges (banana texture)
    for(i = [0:20:100]) {
        rotate([0, 0, i*0.3]) {
            translate([0, 0, i*0.4]) {
                color([0.9, 0.8, 0.15]) {
                    cylinder(h=0.5, r=8.5 - i*0.05, $fn=32);
                }
            }
        }
    }
    
    // Brown spots (overripe areas)
    for(i = [20:15:80]) {
        rotate([0, 0, i*0.3 + 45]) {
            translate([0, 0, i*0.4]) {
                color([0.6, 0.4, 0.1]) {
                    sphere(r=1.5, $fn=8);
                }
            }
        }
    }
}

// Render the banana
banana();
