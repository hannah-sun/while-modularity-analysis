//counting in two ways
original_n = 6;
original_k = 2;

// first way to count
i = 1;
n = original_n;
sum = 0;

while(i <= n) {
    sum = sum + i;
    i = i + 1;
}

// second way to count
k = original_k;
n = original_n + 1;
n_minus_k = n - original_k;
numerator = 1;
denominator = 1; 

// should calculate the denominator of n choose k 
while (k > 0) {
    denominator = k * denominator;
    k = k - 1;
} 

while (n_minus_k > 0) {
    denominator = n_minus_k * denominator;
    n_minus_k = n_minus_k - 1;
} 

// should calculate the numerator of n choose k 
while (n > 0) {
    numerator = n * numerator;
    n = n - 1;
}

choose = numerator/denominator;

// check if the two ways of counting are equal
if (sum == choose){
    print(1); // should be true this is the binomal theorem
}
else {
    print(0);
}
