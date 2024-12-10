#include <iostream>
#include <set>
using namespace std;

void imprimir_map(set<string> a){
    cout << "Tamaño cola " << a.size() << "\n";    
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
    imprimir_map(carros);

    carros.insert("Tesla");
    carros.insert("Mazda");
    carros.insert("Toyota");
    imprimir_map(carros);

    carros.erase("Volvo");
    carros.erase("Mazda");
    carros.insert("Toyota");
    imprimir_map(carros);

    return 0;
}