#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

void imprimir_lista(vector<string> mivector){
    for(string item: mivector){
        cout << item << " ";
    }
    cout << "\n";
}

int main(){
    vector<string> carros = {"Volvo", "BMW", "Ford", "Mazda"};
    cout << "Antes de Ordenar\n";
    imprimir_lista(carros);

    cout << "Ordenado Ascendente\n";
    sort(carros.begin(), carros.end());
    imprimir_lista(carros);
    
    cout << "Ordenado Descendente\n";
    sort(carros.rbegin(), carros.rend());
    imprimir_lista(carros);
    
    return 0;
}