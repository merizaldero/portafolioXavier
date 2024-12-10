#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

void imprimir_lista(vector<int> &mivector){
    for(int item: mivector){
        cout << item << " ";
    }
    cout << "\n";
}

int main(){

    vector<int> numbers = {1, 7, 3, 5, 9, 2};
    cout << "Vector Original :\t";
    imprimir_lista(numbers);
    
    cout << "Vector Copia :\t\t";
    vector<int> copiedNumbers(6);
    copy(numbers.begin(), numbers.end(), copiedNumbers.begin());
    copiedNumbers.back() = 11;
    imprimir_lista(copiedNumbers);

    vector<int> relleno(6);
    cout << "Vector Relleno:\t\t";
    fill(relleno.begin(), relleno.end(), 35);
    imprimir_lista(relleno);

    return 0;

}