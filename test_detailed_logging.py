"""
Test script to verify detailed agent activity logging
"""
import requests
import json
import time

def test_detailed_logging():
    print("🧪 Testing Detailed Agent Activity Logging\n")
    print("="*60)
    
    # Wait for server to be ready
    print("\n⏳ Waiting for backend to start...")
    time.sleep(3)
    
    # Test task that should trigger both Researcher and Coder
    test_task = """
    Calculate the ROI for a solar panel installation:
    - Initial cost: $25,000
    - Monthly savings: $200
    - Lifespan: 20 years
    
    Also research the average ROI for solar panels in the US market.
    """
    
    print(f"\n📋 Test Task:\n{test_task.strip()}\n")
    print("="*60)
    
    try:
        print("\n🚀 Sending request to backend...")
        response = requests.post(
            "http://localhost:8000/api/execute",
            json={"task": test_task, "max_rounds": 20},
            timeout=120
        )
        
        if response.status_code == 200:
            data = response.json()
            
            print("\n✅ Response received!")
            print("="*60)
            
            # Display activity log
            if "activity_log" in data and data["activity_log"]:
                print(f"\n📊 ACTIVITY LOG ({len(data['activity_log'])} entries):\n")
                
                for idx, log in enumerate(data["activity_log"], 1):
                    icon = log.get("icon", "")
                    log_type = log.get("type", "unknown")
                    message = log.get("message", "")
                    
                    print(f"\n{idx}. [{log_type.upper()}] {icon}")
                    print(f"   {message}")
                    print("-" * 60)
                
                # Analyze what we got
                print("\n📈 ANALYSIS:")
                researcher_entries = [l for l in data["activity_log"] if l["type"] == "researcher"]
                coder_entries = [l for l in data["activity_log"] if l["type"] == "coder"]
                
                print(f"   • Researcher entries: {len(researcher_entries)}")
                print(f"   • Coder entries: {len(coder_entries)}")
                
                # Check if we have detailed information
                detailed_researcher = sum(1 for l in researcher_entries if any(
                    keyword in l["message"].lower() 
                    for keyword in ["market research", "data analysis", "trend", "comparative", "•"]
                ))
                detailed_coder = sum(1 for l in coder_entries if any(
                    keyword in l["message"].lower() 
                    for keyword in ["calculation", "roi", "formula", "code:", "performing"]
                ))
                
                print(f"   • Detailed Researcher logs: {detailed_researcher}")
                print(f"   • Detailed Coder logs: {detailed_coder}")
                
                if detailed_researcher > 0 and detailed_coder > 0:
                    print("\n   ✅ SUCCESS: Detailed logging is working!")
                else:
                    print("\n   ⚠️  WARNING: Not seeing detailed logs as expected")
                
            else:
                print("\n❌ No activity log in response!")
            
            # Show result
            if "result" in data:
                print(f"\n📄 RESULT:\n{data['result'][:500]}...")
            
        else:
            print(f"\n❌ Request failed with status {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("\n❌ Could not connect to backend. Is it running on port 8000?")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
    
    print("\n" + "="*60)
    print("🏁 Test complete!\n")

if __name__ == "__main__":
    test_detailed_logging()
