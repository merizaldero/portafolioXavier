#include <iostream>
#include <set>
using namespace std;

void imprimir_set(set<string> a){
    cout << "Tamaño set " << a.size() << "\n";    
    if(! a.empty()){
        for(string item : a){
            cout << item << ' ' ;
        }
        cout << "\n";
    }
    cout << "\n";
}

int main(){
    set<string> carros = {"Volvo", "BMW", "Ford", "BMW", "Mazda"};
    imprimir_set(carros);

    carros.insert("Tesla");
    carros.insert("Mazda");
    carros.insert("Toyota");
    imprimir_set(carros);

    carros.erase("Volvo");
    carros.erase("Mazda");
    carros.insert("Toyota");
    imprimir_set(carros);

    return 0;
}