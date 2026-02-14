#!/usr/bin/env python3
"""
Comprehensive test scenarios for Gemini Image MCP Server.

This script tests various scenarios including different prompts, styles, and edge cases.
"""
import sys
from pathlib import Path
import time

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from config import Config
from gemini_client import GeminiImageClient


class TestScenarios:
    """Collection of test scenarios for image generation."""
    
    def __init__(self):
        """Initialize test scenarios."""
        Config.validate()
        self.client = GeminiImageClient()
        self.results = []
    
    def run_scenario(self, name: str, test_func):
        """Run a test scenario and record results."""
        print(f"\n{'=' * 60}")
        print(f"Scenario: {name}")
        print(f"{'=' * 60}")
        
        start_time = time.time()
        try:
            result = test_func()
            elapsed = time.time() - start_time
            
            if result:
                print(f"\n✓ Scenario passed in {elapsed:.2f} seconds")
                self.results.append((name, True, elapsed))
            else:
                print(f"\n✗ Scenario failed after {elapsed:.2f} seconds")
                self.results.append((name, False, elapsed))
        except Exception as e:
            elapsed = time.time() - start_time
            print(f"\n✗ Scenario error after {elapsed:.2f} seconds: {str(e)}")
            import traceback
            traceback.print_exc()
            self.results.append((name, False, elapsed))
    
    def scenario_1_simple_prompt(self):
        """Test with a simple, straightforward prompt."""
        prompt = "A red apple on a white table"
        result = self.client.generate_image_from_text(prompt)
        return result is not None and result.get('file_path') is not None
    
    def scenario_2_detailed_prompt(self):
        """Test with a detailed, descriptive prompt."""
        prompt = (
            "A serene mountain landscape at sunset with a crystal-clear lake in the foreground, "
            "snow-capped peaks in the background, pine trees lining the shore, "
            "warm orange and pink hues in the sky, watercolor style, 8k resolution"
        )
        result = self.client.generate_image_from_text(prompt)
        return result is not None and len(result.get('image_bytes', b'')) > 0
    
    def scenario_3_artistic_style(self):
        """Test with artistic style specification."""
        prompt = "A portrait of a cat, digital art style, vibrant colors, high detail"
        result = self.client.generate_image_from_text(prompt)
        return result is not None
    
    def scenario_4_abstract_concept(self):
        """Test with abstract or conceptual prompt."""
        prompt = "The concept of time flowing like a river, abstract art, surreal"
        result = self.client.generate_image_from_text(prompt)
        return result is not None
    
    def scenario_5_technical_description(self):
        """Test with technical or specific description."""
        prompt = (
            "A futuristic spaceship, sleek design, metallic surface, "
            "blue energy trails, starfield background, 4k quality"
        )
        result = self.client.generate_image_from_text(prompt)
        return result is not None
    
    def scenario_6_multiple_images(self):
        """Test generating multiple images in sequence."""
        prompts = [
            "A sunny beach scene",
            "A dark forest at night",
            "A modern city skyline"
        ]
        
        all_success = True
        for i, prompt in enumerate(prompts, 1):
            print(f"  Generating image {i}/{len(prompts)}: {prompt[:50]}...")
            result = self.client.generate_image_from_text(prompt)
            if not result:
                all_success = False
            time.sleep(0.5)  # Small delay between requests
        
        return all_success
    
    def scenario_7_long_prompt(self):
        """Test with a very long, detailed prompt."""
        prompt = (
            "A detailed fantasy landscape featuring a medieval castle perched on a cliff, "
            "surrounded by a mystical forest with glowing mushrooms, a dragon flying overhead, "
            "a waterfall cascading down the mountainside, magical creatures in the foreground, "
            "aurora borealis in the night sky, moonlit scene, highly detailed, "
            "fantasy art style, epic composition, cinematic lighting"
        )
        result = self.client.generate_image_from_text(prompt)
        return result is not None and len(prompt) > 200
    
    def scenario_8_short_prompt(self):
        """Test with a very short prompt."""
        prompt = "Sunset"
        result = self.client.generate_image_from_text(prompt)
        return result is not None
    
    def scenario_9_special_characters(self):
        """Test with special characters in prompt."""
        prompt = "A café with 'Welcome' sign & flowers 🌸"
        result = self.client.generate_image_from_text(prompt)
        return result is not None
    
    def scenario_10_custom_filename(self):
        """Test with custom output filename."""
        custom_path = Config.OUTPUT_DIR / f"custom_test_{int(time.time())}.png"
        prompt = "A test image for custom filename"
        result = self.client.generate_image_from_text(
            prompt=prompt,
            output_path=custom_path
        )
        return result is not None and custom_path.exists()
    
    def scenario_11_no_file_save(self):
        """Test generating image without saving to file."""
        prompt = "A memory-only image test"
        result = self.client.generate_image_from_text(
            prompt=prompt,
            save_to_file=False
        )
        return result is not None and result.get('file_path') is None
    
    def scenario_12_base64_output(self):
        """Test that base64 output is valid."""
        prompt = "Testing base64 encoding"
        result = self.client.generate_image_from_text(prompt)
        
        if not result or not result.get('base64'):
            return False
        
        # Try to decode base64
        try:
            import base64
            decoded = base64.b64decode(result['base64'])
            return len(decoded) > 0
        except:
            return False
    
    def run_all(self):
        """Run all test scenarios."""
        print("\n" + "=" * 60)
        print("Comprehensive Test Scenarios")
        print("=" * 60)
        
        scenarios = [
            ("Simple Prompt", self.scenario_1_simple_prompt),
            ("Detailed Prompt", self.scenario_2_detailed_prompt),
            ("Artistic Style", self.scenario_3_artistic_style),
            ("Abstract Concept", self.scenario_4_abstract_concept),
            ("Technical Description", self.scenario_5_technical_description),
            ("Multiple Images", self.scenario_6_multiple_images),
            ("Long Prompt", self.scenario_7_long_prompt),
            ("Short Prompt", self.scenario_8_short_prompt),
            ("Special Characters", self.scenario_9_special_characters),
            ("Custom Filename", self.scenario_10_custom_filename),
            ("No File Save", self.scenario_11_no_file_save),
            ("Base64 Output", self.scenario_12_base64_output),
        ]
        
        for name, func in scenarios:
            self.run_scenario(name, func)
        
        self.print_summary()
    
    def print_summary(self):
        """Print test summary."""
        print("\n" + "=" * 60)
        print("Test Summary")
        print("=" * 60)
        
        total = len(self.results)
        passed = sum(1 for _, success, _ in self.results if success)
        failed = total - passed
        total_time = sum(time for _, _, time in self.results)
        
        print(f"\nTotal Scenarios: {total}")
        print(f"Passed: {passed} ✓")
        print(f"Failed: {failed} {'✗' if failed > 0 else ''}")
        print(f"Total Time: {total_time:.2f} seconds")
        print(f"Average Time: {total_time/total:.2f} seconds per scenario")
        
        print("\nDetailed Results:")
        print("-" * 60)
        for name, success, elapsed in self.results:
            status = "✓ PASS" if success else "✗ FAIL"
            print(f"{status} | {elapsed:6.2f}s | {name}")
        
        print("=" * 60)
        
        if passed == total:
            print("\n🎉 All scenarios passed!")
        else:
            print(f"\n⚠️  {failed} scenario(s) failed. Please review the output above.")


if __name__ == "__main__":
    tester = TestScenarios()
    tester.run_all()
    
    sys.exit(0 if all(r[1] for r in tester.results) else 1)

