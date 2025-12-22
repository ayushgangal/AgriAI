# debug_gemini.py
import os
import google.generativeai as genai
from dotenv import load_dotenv

# 1. Load Key
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

print(f"🔑 Key loaded: {api_key[:10]}..." if api_key else "❌ Key NOT found")

if not api_key:
    exit()

# 2. Configure
genai.configure(api_key=api_key)

print("\n📡 Asking Google for available models...")
try:
    models = list(genai.list_models())
    
    valid_models = []
    print("\n--- AVAILABLE MODELS ---")
    for m in models:
        # We only care about models that can 'generateContent' (chat)
        if 'generateContent' in m.supported_generation_methods:
            print(f"✅ {m.name}")
            valid_models.append(m.name)
        else:
            print(f"   {m.name} (Not for chat)")
    print("------------------------")

    if not valid_models:
        print("\n❌ CRITICAL: Your API Key is valid, but has NO access to any chat models.")
        print("   Solution: Create a new API Key in a new Google Cloud Project.")
        exit()

    # 3. Test the first working model
    best_model = valid_models[0]
    # Prefer flash if available
    for m in valid_models:
        if 'flash' in m:
            best_model = m
            break
            
    print(f"\n🧪 Testing connection with: {best_model}")
    model = genai.GenerativeModel(best_model)
    response = model.generate_content("Hello")
    print(f"🎉 SUCCESS! Response: {response.text}")
    print(f"\n👉 ACTION: Update your 'ai_advisor.py' to use model_name='{best_model}'")

except Exception as e:
    print(f"\n❌ CONNECTION ERROR: {e}")