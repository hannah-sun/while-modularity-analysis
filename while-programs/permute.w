original_n = 6;
original_k = 4;

n = original_n;
k = original_k;
numerator = 1;
denominator = 1; 

k = original_n - original_k;

while (k > 0) {
    denominator = k * denominator;
    
    k = k - 1;
} // should calculate the denominator of n permute k 


while (n > 0) {
    numerator = n * numerator;
    
    n = n - 1;
} // should calculate the numerator of n permute k 

permute = numerator/denominator;

print(permute); // should print n permute k
