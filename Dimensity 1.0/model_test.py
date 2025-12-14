from google import genai

# !!! PASTE YOUR KEY INSIDE THE QUOTES BELOW !!!
MY_API_KEY = "AIzaSyCGEczBdPNbrir9tLWKBw9rCMuqsBksyUI"

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

    # --- TEST B: TRY SENDING A MESSAGE ---
    if found_flash:
        test_model = "gemini-2.0-flash-exp"
    else:
        test_model = "gemini-1.5-flash" # Fallback if 2.0 isn't there

    print(f"\n--- 3. SENDING TEST MESSAGE (Using {test_model}) ---")
    
    response = client.models.generate_content(
        model=test_model,
        contents="Hello! If you can read this, reply with 'System Operational'."
    )
    
    print(f"🤖 REPLY: {response.text}")
    print("\n🎉 CONCLUSION: You are NOT banned. It works!")

except Exception as e:
    print(f"\n💀 FATAL ERROR: {e}")
    print("If this says '403' or 'Permission Denied', generate a NEW key in a NEW project.")