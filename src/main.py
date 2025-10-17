import os
import sys
import argparse
"""
Main entry point for The Machine surveillance system.

This module provides the command-line interface and main controller loop.
It handles tri-authentication, menu navigation, and AI integration.

Features:
- Tri-authentication (password, face, voice).
- Admin menu for system control.
- AI-controlled autonomous modes.
- CLI flags for various operations.

Usage:
- Run as script: python -m src.main
- Use flags like --process-pending, --start-surveillance, etc.
- Interactive menus for manual control.

Dependencies:
- src modules for authentication, admin, AI.
- argparse for CLI parsing.
"""
from src import ai_loader
from src.admin import tri_authenticate, admin_menu
from src.face_recognition import process_pending


def conversational_mode(ai):
    """
    Interactive conversational AI mode with audio synthesis.

    Allows user to chat with AI, generates responses and speaks them.

    Args:
        ai: AI module with generate_response and synthesize_audio methods.
    """
    print("Entering conversational mode. Type 'exit' to quit.")
    while True:
        prompt = input("You: ").strip()
        if prompt.lower() == "exit":
            break
        try:
            response = ai.generate_response(prompt)
            print(f"AI: {response}")
            audio = ai.synthesize_audio(response)
            # Play audio if possible
            try:
                import io
                import wave
                # Assume audio is WAV bytes
                with io.BytesIO(audio) as bio:
                    # This is placeholder; real implementation would play audio
                    print("(Audio synthesized)")
            except Exception:
                print("(Audio synthesis failed)")
        except Exception as e:
            print(f"Error: {e}")


def ai_menu(ai) -> None:
    """AI control sub-menu for surveillance modes."""
    while True:
        print("\nAI Surveillance Modes:")
        print("1) Passive monitoring (log events)")
        print("2) Active alerts (notify on detection)")
        print("3) Event detection (analyze and respond)")
        print("4) Back to main menu")
        choice = input("> ").strip()
        if choice == "1":
            if hasattr(ai, "start_passive_monitoring"):
                try:
                    ai.start_passive_monitoring()
                    print("Passive monitoring started.")
                except Exception as e:
                    print(f"Error: {e}")
            else:
                print("AI does not support passive monitoring.")
        elif choice == "2":
            if hasattr(ai, "start_active_alerts"):
                try:
                    ai.start_active_alerts()
                    print("Active alerts started.")
                except Exception as e:
                    print(f"Error: {e}")
            else:
                print("AI does not support active alerts.")
        elif choice == "3":
            if hasattr(ai, "generate_response") and hasattr(ai, "synthesize_audio"):
                conversational_mode(ai)
            else:
                print("Conversational AI not supported.")
        elif choice == "4":
            break
        else:
            print("Unknown option")


def main_controller() -> None:
    ok = tri_authenticate()
    if not ok:
        print("Authentication failed.")
        sys.exit(2)

    while True:
        print("\nSelect run mode:\n1) Admin system (manual control)\n2) AI controlled (autonomous)\n3) Exit")
        choice = input("> ").strip()
        if choice == "1":
            admin_menu()
        elif choice == "2":
            ai = ai_loader.get_ai()
            if ai is None:
                print("AI mode unavailable.")
                continue
            ai_menu(ai)
        elif choice == "3":
            print("Exiting.")
            break
        else:
            print("Unknown option")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="The Machine - AI Surveillance System")
    parser.add_argument("--process-pending", action="store_true", help="Run process_pending() once and exit")
    parser.add_argument("--start-surveillance", action="store_true", help="Start surveillance mode")
    parser.add_argument("--stop-surveillance", action="store_true", help="Stop surveillance mode")
    parser.add_argument("--logs", action="store_true", help="View event logs")
    parser.add_argument("--status", action="store_true", help="Show system status")
    parser.add_argument("--retrain", nargs='?', const="daily", help="Retrain AI model with schedule (default daily)")
    args = parser.parse_args()

    if args.process_pending:
        try:
            processed = process_pending()
            print(f"Processed {processed} pending images")
        except Exception:
            print("Error processing pending images.")
        sys.exit(0)
    elif args.start_surveillance:
        from src.admin import start_surveillance
        start_surveillance()
        sys.exit(0)
    elif args.stop_surveillance:
        from src.admin import stop_surveillance
        stop_surveillance()
        sys.exit(0)
    elif args.logs:
        from src.admin import view_logs
        view_logs()
        sys.exit(0)
    elif args.status:
        from src.admin import system_status
        system_status()
        sys.exit(0)
    elif args.retrain:
        ai = ai_loader.get_ai()
        if ai and hasattr(ai, "retrain_model"):
            try:
                # Placeholder data; in real use, load from somewhere
                data = [{"text": "example", "label": "positive"}]
                ai.retrain_model(data, args.retrain)
                print("Retraining completed.")
            except Exception as e:
                print(f"Retraining error: {e}")
        else:
            print("AI retraining not supported.")
        sys.exit(0)

    main_controller()