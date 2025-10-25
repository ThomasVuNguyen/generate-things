// Generated OpenSCAD code for an orange
// This is an example of what the AI might generate

module orange() {
    // Main orange body
    color([1.0, 0.5, 0.0]) {
        difference() {
            // Base sphere
            sphere(r=22, $fn=64);
            
            // Small indentation at the top
            translate([0, 0, 18]) {
                cylinder(h=8, r=6, $fn=32);
            }
        }
    }
    
    // Orange peel texture (bumpy surface)
    for(i = [0:15:360]) {
        for(j = [0:15:180]) {
            rotate([j, 0, i]) {
                translate([0, 0, 18 + 3*sin(i*2)*cos(j*2)]) {
                    color([1.0, 0.6, 0.1]) {
                        sphere(r=1.5, $fn=12);
                    }
                }
            }
        }
    }
    
    // Stem area
    color([0.3, 0.2, 0.1]) {
        translate([0, 0, 22]) {
            cylinder(h=3, r=4, $fn=16);
        }
    }
    
    // Small stem
    color([0.2, 0.15, 0.1]) {
        translate([0, 0, 25]) {
            cylinder(h=4, r1=1.5, r2=0.8, $fn=12);
        }
    }
    
    // Leaf
    color([0.2, 0.7, 0.2]) {
        translate([2, 0, 27]) {
            rotate([0, 0, 30]) {
                scale([1, 0.4, 1]) {
                    sphere(r=4, $fn=16);
                }
            }
        }
    }
}

// Render the orange
orange();
