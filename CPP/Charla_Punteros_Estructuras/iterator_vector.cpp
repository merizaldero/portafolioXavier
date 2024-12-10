#include <iostream>
#include <vector>
using namespace std;

int main(){

    vector<string> carros = {"Volvo", "BMW", "Ford", "Mazda"};

    vector<string>::iterator it;

    for (it = carros.begin(); it != carros.end(); ++ it) {
        cout << *it << " ";
    }
    cout << "\n";

    it = carros.begin();
    *it = "Andino";
    *(it + 1) = "Citroen";

    for (auto it2 = carros.begin(); it2 != carros.end(); ++ it2) {
        cout << *it2 << " ";
    }
    cout << "\n";

    auto it3 = carros.end();
    *(it3 - 1) = "Nissan";
    *(it3 - 2) = "Chevrolet";

    for (auto it4 = carros.begin(); it4 != carros.end(); ++ it4) {
        cout << *it4 << " ";
    }
    cout << "\n";

    for(string carro: carros){
        cout << carro << " ";
    }   

    cout << "\n";

    for (auto it5 = carros.rbegin(); it5 != carros.rend(); ++ it5) {
        cout << *it5 << " ";
    }
    cout << "\n";

    return 0;
}