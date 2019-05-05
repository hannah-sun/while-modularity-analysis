n = 21;

// finds 21st Fibonacci number (1st number is 0, 2nd is 1, and so on)

n1 = 0;
n2 = 1;

if (n == 1) {
	print(0);
}

if (n > 1 and n == 2) {
	print(1);
}

if (n > 2) {
    count = 2; 

    while (count < n) {
    	nth = n1 + n2;
    	n1 = n2;
    	n2 = nth;
    	count = count + 1;
    }
    
    print(nth);
}

n = 25;

// finds 25th Fibonacci number (1st number is 0, 2nd is 1, and so on)

n_1 = 0;
n_2 = 1;
n_fib = 0;

count = 2; 

while (count < n) {
	n_fib = n_1 + n_2;
	n_1 = n_2;
	n_2 = n_fib;
	count = count + 1;
}

print(n_fib);

