// Generated OpenSCAD code for an apple
// This is an example of what the AI might generate

module apple() {
    // Main apple body with slight asymmetry for realism
    color([0.8, 0.2, 0.2]) {
        difference() {
            // Base sphere with scaling for apple shape
            scale([1, 1, 1.2]) {
                sphere(r=25, $fn=64);
            }
            
            // Indentation at the top for stem
            translate([0, 0, 20]) {
                cylinder(h=10, r=8, $fn=32);
            }
            
            // Small indentation at the bottom
            translate([0, 0, -25]) {
                cylinder(h=5, r=3, $fn=16);
            }
        }
    }
    
    // Stem
    color([0.4, 0.2, 0.1]) {
        translate([0, 0, 30]) {
            rotate([0, 0, 15]) {
                cylinder(h=8, r1=2, r2=1, $fn=16);
            }
        }
    }
    
    // Leaf
    color([0.2, 0.6, 0.2]) {
        translate([3, 0, 35]) {
            rotate([0, 0, 45]) {
                scale([1, 0.3, 1]) {
                    sphere(r=6, $fn=32);
                }
            }
        }
    }
    
    // Surface texture (small bumps)
    for(i = [0:5:360]) {
        for(j = [0:10:180]) {
            rotate([j, 0, i]) {
                translate([0, 0, 20 + 5*sin(i)*cos(j)]) {
                    color([0.9, 0.3, 0.3]) {
                        sphere(r=0.5, $fn=8);
                    }
                }
            }
        }
    }
}

// Render the apple
apple();
