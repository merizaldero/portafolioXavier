#include <iostream>
#include <list>
using namespace std;

void imprimir_lista(list<string> lista){
    for (string item : lista) {
        cout << item << " ";
    }
    cout << "\nLista tiene " << lista.size() << " elementos\n";
}

int main(){
    list<string> carros = {"Volvo", "BMW", "Ford", "Mazda"};
    
    if(carros.empty() ){
        cout << "El vector esta vacio";
    } else {
        imprimir_lista(carros);
    }

    carros.front() = "Opel";
    carros.back() = "Andino";
    imprimir_lista(carros);

    carros.push_front("Tesla");
    carros.push_back("VW");
    imprimir_lista(carros);

    carros.pop_front();
    carros.pop_back();
    imprimir_lista(carros);

    return 0;
}
