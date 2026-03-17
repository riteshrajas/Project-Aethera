"""
Example: Export and Manage WhatsApp Contacts with Aethera
Demonstrates how to use the WhatsApp integration to export contacts to JSON
"""

from wrapper.integrations.whatsapp.aethera_client import get_client
import json
from pathlib import Path


def example_export_all_contacts():
    """Export all WhatsApp contacts to data folder as JSON"""
    whatsapp = get_client()
    
    # Wait for connection
    if not whatsapp.wait_for_connection(timeout=30):
        print("Failed to connect to WhatsApp")
        return
    
    print("✓ Connected to WhatsApp")
    
    # Get all contacts
    contacts = whatsapp.get_all_contacts()
    print(f"\n📋 Found {len(contacts)} contacts")
    
    # Print summary
    for i, contact in enumerate(contacts[:5], 1):
        print(f"  {i}. {contact['name']} ({contact['number']})")
    
    if len(contacts) > 5:
        print(f"  ... and {len(contacts) - 5} more")
    
    # Export to JSON file in data folder
    print("\n💾 Exporting contacts to data folder...")
    export_result = whatsapp.export_contacts_to_json()
    
    print(f"✓ Exported successfully!")
    print(f"  Filename: {export_result['filename']}")
    print(f"  Total contacts: {export_result['contactCount']}")
    
    return export_result


def example_load_latest_contacts():
    """Load the latest exported contacts from data folder"""
    whatsapp = get_client()
    
    print("📂 Loading latest exported contacts...")
    
    try:
        latest_export = whatsapp.get_latest_contacts_export()
        
        print(f"\n✓ Loaded {latest_export['totalContacts']} contacts")
        print(f"  Exported at: {latest_export['exportedAt']}")
        
        # Print contacts
        for i, contact in enumerate(latest_export['contacts'][:10], 1):
            status = "👤"
            if contact['isContact']:
                status = "📱"
            print(f"  {status} {contact['name']} - {contact['number']}")
        
        return latest_export
    except Exception as e:
        print(f"✗ Error: {e}")
        return None


def example_list_all_exports():
    """List all exported contact files"""
    whatsapp = get_client()
    
    print("📋 Listing all exported contact files...\n")
    
    exports = whatsapp.list_contacts_exports()
    
    if not exports:
        print("  No exported files found")
        return
    
    for i, export in enumerate(exports, 1):
        print(f"  {i}. {export['filename']}")


def example_analyze_contacts():
    """Analyze contacts and create summary stats"""
    whatsapp = get_client()
    
    if not whatsapp.wait_for_connection(timeout=30):
        print("Failed to connect to WhatsApp")
        return
    
    # Get all contacts
    contacts = whatsapp.get_all_contacts()
    
    # Create stats
    stats = {
        "total_contacts": len(contacts),
        "contact_users": sum(1 for c in contacts if c['isContact']),
        "users": sum(1 for c in contacts if c['isUser']),
        "by_status": {
            "contacts": sum(1 for c in contacts if c['isContact']),
            "users": sum(1 for c in contacts if c['isUser']),
            "me": sum(1 for c in contacts if c['isMe'])
        }
    }
    
    print("📊 Contact Analysis")
    print(f"  Total contacts: {stats['total_contacts']}")
    print(f"  Saved contacts: {stats['contact_users']}")
    print(f"  Active users: {stats['users']}")
    
    # Export
    export_result = whatsapp.export_contacts_to_json()
    
    print(f"\n💾 Exported to: data/{export_result['filename']}")
    
    return stats


def example_integration_with_aethera():
    """
    Example of integrating with Aethera core modules
    """
    from core.information_management.data_analysis import analyze_text_frequency
    
    whatsapp = get_client()
    
    if not whatsapp.wait_for_connection():
        print("WhatsApp not connected")
        return
    
    # Export all contacts
    export_result = whatsapp.export_contacts_to_json()
    exported_file = export_result['filename']
    
    print(f"Contacts exported to: data/{exported_file}")
    
    # Load the exported data
    latest = whatsapp.get_latest_contacts_export()
    contacts = latest['contacts']
    
    # Extract all contact names
    contact_names = [c['name'] for c in contacts if c['name']]
    
    # Use Aethera's text analysis on contact names
    all_names_text = " ".join(contact_names)
    frequency = analyze_text_frequency(all_names_text)
    
    print(f"\n📈 Contact Name Analysis:")
    for word, count in list(frequency.items())[:5]:
        print(f"  '{word}': {count} occurrences")


if __name__ == "__main__":
    print("=" * 60)
    print("Aethera WhatsApp Contacts Export Examples")
    print("=" * 60)
    
    # Run examples
    print("\n1️⃣  EXPORT ALL CONTACTS")
    print("-" * 60)
    example_export_all_contacts()
    
    print("\n\n2️⃣  LOAD LATEST EXPORTED CONTACTS")
    print("-" * 60)
    example_load_latest_contacts()
    
    print("\n\n3️⃣  LIST ALL EXPORTS")
    print("-" * 60)
    example_list_all_exports()
    
    print("\n\n4️⃣  ANALYZE CONTACTS")
    print("-" * 60)
    example_analyze_contacts()
    
    print("\n" + "=" * 60)
