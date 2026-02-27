#include <iostream>
#include <vector>
#include <string>
#include <fstream>
#include <sstream>
#include <algorithm>

class TextProcessor {
public:
    struct Chunk {
        int id;
        std::string content;
    };

    // Dosyayı okur ve satır satır temizler
    std::string readFile(const std::string& filename) {
        std::ifstream file(filename);
        std::stringstream buffer;
        if (file.is_open()) {
            buffer << file.rdbuf();
            file.close();
        }
        return buffer.str();
    }

    // Metni belirli bir uzunlukta (max_size) parçalara böler
    std::vector<Chunk> createChunks(const std::string& text, size_t max_size) {
        std::vector<Chunk> chunks;
        size_t pos = 0;
        int current_id = 0;

        while (pos < text.length()) {
            std::string sub = text.substr(pos, max_size);
            
            // Kelimeyi ortadan bölmemek için en yakın boşluğu bul (Basit Optimizasyon)
            if (pos + max_size < text.length()) {
                size_t last_space = sub.find_last_of(" \n\t");
                if (last_space != std::string::npos) {
                    sub = sub.substr(0, last_space);
                }
            }

            chunks.push_back({current_id++, sub});
            pos += sub.length() + 1; // Bir sonraki boşluktan devam et
        }
        return chunks;
    }
};

int main() {
    TextProcessor proc;
    std::string content = proc.readFile("veri.txt"); // İşlenecek dosya
    
    // 500 karakterlik parçalara bölüyoruz
    auto chunks = proc.createChunks(content, 500);

    std::cout << "Toplam parca sayisi: " << chunks.size() << std::endl;
    if(!chunks.empty()) {
        std::cout << "Ilk parca ornegi:\n" << chunks[0].content << std::endl;
    }
system("pause");
    return 0;
}