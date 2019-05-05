x = 3;
y = 10;

original_n = 4;
original_k = 0;
sum = 0;

xy_sum = 1;
n = original_n;

while (n > 0){
    xy_sum = xy_sum * (x + y);
    
    n = n - 1;
}
print(xy_sum);

while (original_n >= original_k) {
    n = original_n;
    k = original_k;
    n_minus_k = original_n - original_k;
    numerator = 1;
    denominator = 1; 

    while (k > 0) {
        denominator = k * denominator;
        
        k = k - 1;
    } 

    while (n_minus_k > 0) {
        denominator = n_minus_k * denominator;
        
        n_minus_k = n_minus_k - 1;
    } // should calculate the denominator of n choose k 

    while (n > 0) {
        numerator = n * numerator;
        
        n = n - 1;
    } // should calculate the numerator of n choose k 

    choose = numerator/denominator; // n choose k
    print(choose);

    x_pow = 1;
    y_pow = 1;

    k = original_k;
    n_minus_k = original_n - original_k;

    while ( k > 0 or n_minus_k > 0) {
        if (k != 0) {
            x_pow = x * x_pow;
            k = k - 1;
        }
        
        if (n_minus_k != 0) {
            y_pow = y * y_pow;
            n_minus_k = n_minus_k - 1;
        }
    }

    // x_pow should be x^(n-k)
    // y_pow should be y^k
    print(choose * x_pow * y_pow);
    sum = sum + (choose * x_pow * y_pow);

    original_k = original_k + 1;
}

print(sum);

if (xy_sum == sum){
    print(1); // should be true this is the binomal theorem
}
else {
    print(0);
}
