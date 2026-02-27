import os
import json
import sys

# Türkçe karakter desteği (Windows terminali için)
if sys.platform == "win32":
    import codecs
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

# Yeni nesil importlar (Hata vermez)
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate

# 1. ARAÇ (TOOL) TANIMI
@tool
def search_cpp_data(query: str) -> str:
    """C++ motorunun ürettiği JSON dosyasında Türkçe karakter uyumlu arama yapar."""
    # Dosya yolunu kontrol et
    file_path = "processed_data.json" # C++ ile aynı klasördeyse böyle kalsın
    
    if not os.path.exists(file_path):
        return "Hata: Veri dosyası bulunamadı. Lütfen önce C++ kodunu çalıştırın."

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        # Türkçe karakter uyumlu arama
        q_low = query.lower().replace('İ', 'i').replace('I', 'ı')
        results = [item['content'] for item in data if q_low in item['content'].lower()]
        
        return "\n---\n".join(results[:3]) if results else "Bilgi bulunamadı."
    except Exception as e:
        return f"Hata: {str(e)}"

# 2. AYARLAR
os.environ["OPENAI_API_KEY"] = "sk-..." # Kendi anahtarını buraya yaz

# 3. MODERN AGENT KURULUMU
llm = ChatOpenAI(model="gpt-4o", temperature=0)
tools = [search_cpp_data]

# En güncel prompt şablonu
prompt = ChatPromptTemplate.from_messages([
    ("system", "Sen yardımcı bir asistansın. Araçları kullanarak soruları Türkçe cevapla."),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
])

# Agent ve Çalıştırıcıyı oluştur
agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# 4. ÇALIŞTIRMA
if __name__ == "__main__":
    print("--- Sistem Başlatıldı ---")
    try:
        agent_executor.invoke({"input": "Dosyadaki verilere bakarak kısa bir özet çıkar."})
    except Exception as e:
        print(f"Hata: {e}")