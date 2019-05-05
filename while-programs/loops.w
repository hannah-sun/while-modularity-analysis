x = 2;
y = 0;
z = -5;

temp = 1;

a = x;
b = y;

while (z < x + y) {
	z = z + 1;
}

// z should be 2

if (temp != z) {
	temp = z;	// should be 2
}

a = a << 2; 	// should be 8

if (a != b) {
	b = a;		// should be 8
}

a = 100 - b;	// should be 92
b = temp;		// should be 2

c = a + b;

x = y + z;
