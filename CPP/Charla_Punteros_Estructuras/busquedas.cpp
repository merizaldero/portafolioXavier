#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

int main(){

    // Create a vector called numbers that will store integers
    vector<int> numbers = {1, 7, 3, 5, 9, 2};

    cout << "Busqueda find()\n" ;
    auto it = find(numbers.begin(), numbers.end(), 3);
    if( it == numbers.end() ){
        cout << "Valor no encontrado.\n";
    }else{
        cout << "Valor encontrado: " << *it << " .\n";
    }
    
    cout << "Busqueda upper_bound()\n" ;
    sort(numbers.begin(), numbers.end());
    it = upper_bound(numbers.begin(), numbers.end(), 5);
    if( it == numbers.end() ){
        cout << "Valor no encontrado.\n";
    }else{
        cout << "Valor encontrado: " << *it << " .\n";
    }

    cout << "Busqueda min_element()\n" ;
    it = min_element(numbers.begin(), numbers.end());
    if( it == numbers.end() ){
        cout << "Valor no encontrado.\n";
    }else{
        cout << "Minimo: " << *it << " .\n";
    }
    
    cout << "Busqueda max_element()\n" ;
    it = max_element(numbers.begin(), numbers.end());
    if( it == numbers.end() ){
        cout << "Valor no encontrado.\n";
    }else{
        cout << "Maximo: " << *it << " .\n";
    }
    
    return 0;
}