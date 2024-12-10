#include <iostream>
#include <deque>
using namespace std;

void imprimir_cola(deque<string> cola){
    cout << "Tamaño cola " << cola.size() << "\n";    
    if(! cola.empty()){
        cout << "inicio Cola: " << cola.front() << "\n";
        cout << "Ultimo Cola: " << cola.back() << "\n";
        for(int i = 0; i < cola.size(); i++){
            cout << cola.at(i) << ' ' ;
        }
        cout << "\n";
    }
    cout << "\n";
}

int main(){
    deque<string> carros = {"Volvo", "BMW", "Ford", "Mazda"};
    imprimir_cola(carros);

    carros.front() = "Kia";
    carros.back() = "Toyota";
    imprimir_cola(carros);

    carros[1] = "Opel";
    carros.at(2) = "Andino";
    imprimir_cola(carros);

    carros.push_front("Tesla");
    carros.push_back("VW");
    imprimir_cola(carros);

    carros.pop_front();
    carros.pop_back();
    imprimir_cola(carros);

    return 0;
}