from google import genai

# !!! PASTE YOUR KEY INSIDE THE QUOTES BELOW !!!
MY_API_KEY = ""

print("--- 1. CONNECTING ---")
try:
    # Initialize the new Client
    client = genai.Client(api_key=MY_API_KEY)
    print("✅ Client created successfully.")

    # --- TEST A: CHECK AVAILABLE MODELS ---
    print("\n--- 2. CHECKING MODELS ---")
    print("Asking Google: 'What models can I use?'...")
    
    found_flash = False
    count = 0
    
    # List models
    for model in client.models.list():
        print(f"  • Found: {model.name}")
        count += 1
        if "gemini-2.0-flash-exp" in model.name:
            found_flash = True

    if count == 0:
        print("❌ ERROR: No models found. Your key is valid, but has NO access permissions.")
    else:
        print(f"✅ SUCCESS: Found {count} models available to you.")

except Exception as e:
    print(f"\n💀 FATAL ERROR: {e}")
    print("Permission Denied, generate a NEW key in a NEW project.")