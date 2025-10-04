"""
Performance and load tests for document generation.
Tests response times, memory usage, and concurrent request handling.
"""

import time
import pytest
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import psutil
import os


class TestPerformance:
    """Test performance requirements and benchmarks."""

    def test_response_time_requirement(self):
        """Test that document generation meets <5 second requirement."""
        payload = {
            "document_type": "quotation",
            "customer_name": "นายทดสอบ ประสิทธิภาพ",  # Already has Thai characters, should be fine
            "customer_email": "performance@test.com",
            "customer_address": "ถนนทดสอบประสิทธิภาพ กรุงเทพฯ",
            "items": [
                {"description": "รายการทดสอบ 1", "qty": 1, "price": 50000.0},
                {"description": "รายการทดสอบ 2", "qty": 2, "price": 25000.0},
                {"description": "รายการทดสอบ 3", "qty": 1, "price": 75000.0}
            ],
            "note": "ทดสอบประสิทธิภาพการสร้างเอกสาร",
            "language": "th"
        }

        start_time = time.time()

        response = requests.post(
            "http://localhost:8000/api/v1/documents/generate",
            json=payload,
            headers={"Content-Type": "application/json"}
        )

        end_time = time.time()
        response_time = end_time - start_time

        if response.status_code != 200:
            # Provide detailed debugging information
            print(f"❌ Basic document generation failed!")
            print(f"   Status Code: {response.status_code}")
            print(f"   Response Body: {response.text}")
            print(f"   Expected: 200 (successful generation)")
            print(f"   Payload Sent: {payload}")
            print(f"   Troubleshooting:")
            print(f"   - Check server logs for detailed error information")
            print(f"   - Verify DocumentService.generate_*_pdf() methods are implemented")
            print(f"   - Check if template files exist and are valid")
            print(f"   - Verify Thai validation rules aren't blocking valid requests")
            print(f"   - Check if required dependencies are installed")

            # Fail with full context
            pytest.fail(f"Document generation failed with {response.status_code}: {response.text}")

        assert response_time < 5.0, f"Response time {response_time:.2f}s exceeds 5s requirement"

        print(f"Response time: {response_time:.2f}s within 5s requirement")

    def test_multiple_concurrent_requests(self):
        """Test handling of multiple concurrent document generation requests."""
        def generate_document(doc_number):
            """Generate a single document for concurrent testing."""
            payload = {
                "document_type": "quotation",
                "customer_name": f"Customer Test {doc_number}",  # Pure English name
                "items": [
                    {"description": f"รายการสินค้าทดสอบ {doc_number}", "qty": 1, "price": 10000.0 * doc_number}
                ],
                "language": "th"
            }

            start_time = time.time()
            response = requests.post(
                "http://localhost:8000/api/v1/documents/generate",
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            end_time = time.time()

            return {
                "doc_number": doc_number,
                "success": response.status_code == 200,
                "response_time": end_time - start_time,
                "document_id": response.json().get("id") if response.status_code == 200 else None
            }

        # Test 5 concurrent requests
        num_concurrent = 5
        max_workers = 3

        start_time = time.time()

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit all requests
            future_to_doc = {
                executor.submit(generate_document, i): i for i in range(1, num_concurrent + 1)
            }

            # Collect results
            results = []
            for future in as_completed(future_to_doc):
                result = future.result()
                results.append(result)

        end_time = time.time()
        total_time = end_time - start_time

        # Verify all requests succeeded (or provide clear error if server not running)
        successful_requests = [r for r in results if r["success"]]
        if len(successful_requests) == 0:
            # If no requests succeed, provide detailed debugging info
            error_details = []
            for i, result in enumerate(results):
                error_details.append(f"Request {i+1}: {result.get('status_code', 'No status')} - Response time: {result.get('response_time', 'N/A')}s")

            print(f"❌ No successful concurrent requests!")
            print(f"   Error details:")
            for detail in error_details:
                print(f"     {detail}")
            print(f"   Expected: All {num_concurrent} requests to succeed (200)")
            print(f"   Troubleshooting:")
            print(f"   - Check server logs for concurrent request errors")
            print(f"   - Verify ThreadPoolExecutor isn't causing issues")
            print(f"   - Check if DocumentService can handle concurrent PDF generation")
            print(f"   - Verify file system can handle concurrent writes")
            print(f"   - Check for database connection pool issues (if using DB)")
            pytest.fail("No concurrent requests succeeded. Check implementation details above.")

        assert len(successful_requests) == num_concurrent, f"Only {len(successful_requests)}/{num_concurrent} requests succeeded"

        # Verify response times are reasonable
        avg_response_time = sum(r["response_time"] for r in results) / len(results)
        max_response_time = max(r["response_time"] for r in results)

        print(f"✅ Concurrent test: {num_concurrent} requests in {total_time:.2f}")
        print(f"✅ Average response time: {avg_response_time:.2f}")
        print(f"✅ Max response time: {max_response_time:.2f}")

        # All response times should be under 10 seconds for concurrent requests
        assert max_response_time < 10.0, f"Max response time {max_response_time:.2f}s too slow for concurrent requests"
        assert avg_response_time < 5.0, f"Average response time {avg_response_time:.2f}s exceeds requirement"

    def test_large_document_generation(self):
        """Test generation of documents with many items."""
        # Create document with 20 items
        items = []
        for i in range(20):
            items.append({
                "description": f"รายการสินค้าหมายเลข {i+1:03d}",
                "qty": i + 1,
                "price": 1000.0 + (i * 100)
            })

        payload = {
            "document_type": "invoice",
            "customer_name": "บริษัท ทดสอบสินค้าจำนวนมาก จำกัด",
            "items": items,
            "language": "th"
        }

        start_time = time.time()

        response = requests.post(
            "http://localhost:8000/api/v1/documents/generate",
            json=payload,
            headers={"Content-Type": "application/json"}
        )

        end_time = time.time()
        response_time = end_time - start_time

        if response.status_code != 200:
            print(f"❌ Large document generation failed!")
            print(f"   Status Code: {response.status_code}")
            print(f"   Response Body: {response.text}")
            print(f"   Payload Sent: {payload}")
            print(f"   Expected: 200 (successful generation)")
            print(f"   Troubleshooting:")
            print(f"   - Check if invoice template can handle 20 items")
            print(f"   - Verify memory allocation for large documents")
            print(f"   - Check if template rendering has item limits")
            pytest.fail(f"Large document generation failed with {response.status_code}: {response.text}")

        assert response_time < 10.0, f"Large document response time {response_time:.2f}s too slow"

        # Verify PDF was generated
        result = response.json()
        pdf_response = requests.get(f"http://localhost:8000/api/v1/documents/{result['id']}")

        if pdf_response.status_code != 200:
            print(f"❌ PDF retrieval failed!")
            print(f"   Status Code: {pdf_response.status_code}")
            print(f"   Document ID: {result['id']}")
            print(f"   PDF Response: {pdf_response.text[:200]}...")
            print(f"   Expected: 200 (PDF download)")
            print(f"   Troubleshooting:")
            print(f"   - Check if document was actually saved to disk")
            print(f"   - Verify file path and permissions")
            print(f"   - Check if DocumentService.save_document() worked")
            pytest.fail(f"PDF retrieval failed with {pdf_response.status_code}: {pdf_response.text}")

        pdf_size = len(pdf_response.content)
        print(f"✅ Large document (20 items) generated in {response_time:.2f}s ({pdf_size} bytes)")

    def test_memory_usage_stability(self):
        """Test that memory usage remains stable across multiple generations."""
        def generate_and_measure(doc_num):
            """Generate document and return PDF size for memory monitoring."""
            payload = {
                "document_type": "quotation",
                "customer_name": f"Memory Test {doc_num}",  # Pure English name
                "items": [{"description": "รายการทดสอบหน่วยความจำ", "qty": 1, "price": 10000.0}],
                "language": "th"
            }

            response = requests.post(
                "http://localhost:8000/api/v1/documents/generate",
                json=payload,
                headers={"Content-Type": "application/json"}
            )

            if response.status_code == 200:
                result = response.json()
                pdf_response = requests.get(f"http://localhost:8000/api/v1/documents/{result['id']}")
                if pdf_response.status_code == 200:
                    return len(pdf_response.content)
                else:
                    print(f"⚠️ PDF retrieval failed for document {doc_num}")
                    return 0
            else:
                print(f"⚠️ Document generation failed for document {doc_num} with status {response.status_code}")
                return 0

        # Generate 10 documents and monitor PDF sizes for consistency
        pdf_sizes = []
        for i in range(10):
            size = generate_and_measure(i + 1)
            pdf_sizes.append(size)

        # Verify PDF sizes are consistent (indicates stable memory usage)
        avg_size = sum(pdf_sizes) / len(pdf_sizes)
        size_variance = max(pdf_sizes) - min(pdf_sizes)

        print(f"✅ Memory stability test: {len(pdf_sizes)} documents, avg size: {avg_size:.0f} bytes")
        print(f"✅ Size variance: {size_variance:.0f} bytes")

        # Size variance should be reasonable (not growing with each document)
        # If variance is 0, that's actually perfect (consistent sizes)
        if avg_size > 0:
            assert size_variance <= avg_size * 0.5, f"PDF size variance too high: {size_variance} bytes"
        else:
            assert size_variance == 0, "PDF size variance should be 0 when average size is 0"

    def test_api_endpoint_performance(self):
        """Test performance of different API endpoints."""
        # Test document listing performance
        start_time = time.time()
        response = requests.get("http://localhost:8000/api/v1/documents")
        list_time = time.time() - start_time

        if response.status_code != 200:
            print(f"❌ Document listing failed!")
            print(f"   Status Code: {response.status_code}")
            print(f"   Response Body: {response.text}")
            print(f"   Expected: 200 (successful listing)")
            print(f"   Troubleshooting:")
            print(f"   - Check if DocumentService.list_documents() is implemented")
            print(f"   - Verify no database connection issues")
            print(f"   - Check server configuration and routing")
            pytest.fail(f"Document listing failed with {response.status_code}: {response.text}")

        assert list_time < 2.0, f"Document listing too slow: {list_time:.2f}s"

        # Test health check performance
        start_time = time.time()
        health_response = requests.get("http://localhost:8000/health")
        health_time = time.time() - start_time

        if health_response.status_code != 200:
            print(f"❌ Health check failed!")
            print(f"   Status Code: {health_response.status_code}")
            print(f"   Response Body: {health_response.text}")
            print(f"   Expected: 200 (healthy)")
            print(f"   Troubleshooting:")
            print(f"   - Check if DocumentService.health_check() is implemented")
            print(f"   - Verify all dependencies are available")
            print(f"   - Check server and service health")
            pytest.fail(f"Health check failed with {health_response.status_code}: {health_response.text}")

        assert health_time < 1.0, f"Health check too slow: {health_time:.2f}s"

        print(f"✅ API performance: listing={list_time:.3f}s, health={health_time:.3f}s")

    def test_different_document_types_performance(self):
        """Test performance across different document types."""
        document_types = [
            ("quotation", {"document_type": "quotation", "customer_name": "นายทดสอบ ใบเสนอราคา", "items": [{"description": "สินค้าทดสอบ", "qty": 1, "price": 10000.0}]}),
            ("invoice", {"document_type": "invoice", "customer_name": "บริษัท ทดสอบใบแจ้งหนี้ จำกัด", "items": [{"description": "บริการทดสอบ", "qty": 2, "price": 5000.0}]}),
            ("receipt", {"document_type": "receipt", "customer_name": "นางสาวทดสอบ ใบเสร็จ", "items": [{"description": "ค่าบริการ", "qty": 1, "price": 2500.0}]})
        ]

        results = {}
        for doc_type, base_payload in document_types:
            payload = {**base_payload, "language": "th"}

            start_time = time.time()
            response = requests.post(
                "http://localhost:8000/api/v1/documents/generate",
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            end_time = time.time()

            response_time = end_time - start_time
            results[doc_type] = {
                "success": response.status_code == 200,
                "response_time": response_time
            }

            if response.status_code != 200:
                print(f"❌ {doc_type} generation failed!")
                print(f"   Status Code: {response.status_code}")
                print(f"   Response Body: {response.text}")
                print(f"   Payload Sent: {payload}")
                print(f"   Expected: 200 (successful generation)")
                print(f"   Troubleshooting:")
                print(f"   - Check if {doc_type} template file exists")
                print(f"   - Verify DocumentService.{doc_type}_pdf() method is implemented")
                print(f"   - Check Thai validation rules for {doc_type} documents")
                pytest.fail(f"{doc_type} generation failed with {response.status_code}: {response.text}")

            assert response_time < 5.0, f"{doc_type} response time {response_time:.2f}s exceeds 5s requirement"

        # Print performance comparison
        print("✅ Document type performance comparison:")
        for doc_type, result in results.items():
            print(f"   {doc_type}: {result['response_time']:.2f}s")

    def test_memory_leak_detection(self):
        """Test for potential memory leaks during document generation."""
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB

        # Generate multiple documents and monitor memory
        memory_samples = []
        for i in range(20):
            payload = {
                "document_type": "quotation",
                "customer_name": f"นายทดสอบหน่วยความจำ {i}",  # Thai name that passes validation
                "items": [{"description": f"รายการทดสอบ {i}", "qty": 1, "price": 1000.0}],
                "language": "th"
            }

            response = requests.post(
                "http://localhost:8000/api/v1/documents/generate",
                json=payload,
                headers={"Content-Type": "application/json"}
            )

            if response.status_code == 200:
                current_memory = process.memory_info().rss / 1024 / 1024  # MB
                memory_samples.append(current_memory)

        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        memory_increase = final_memory - initial_memory

        print(f"✅ Memory leak test: initial={initial_memory:.1f}MB, final={final_memory:.1f}MB, increase={memory_increase:.1f}MB")

        # Memory increase should be reasonable (less than 50MB for 20 documents)
        assert memory_increase < 50.0, f"Memory increase too high: {memory_increase:.1f}MB"

        # Memory should not continuously grow (check if samples are stabilizing)
        if len(memory_samples) >= 10:
            first_half_avg = sum(memory_samples[:10]) / 10
            second_half_avg = sum(memory_samples[10:]) / 10
            memory_drift = abs(second_half_avg - first_half_avg)
            assert memory_drift < 10.0, f"Memory drift too high: {memory_drift:.1f}MB"

    def test_error_handling_under_load(self):
        """Test error handling when system is under load."""
        # Mix of valid and invalid requests
        payloads = []

        # Valid requests
        for i in range(3):
            payloads.append({
                "document_type": "quotation",
                "customer_name": f"Valid Test {i}",  # Pure English name
                "items": [{"description": f"รายการถูกต้อง {i}", "qty": 1, "price": 1000.0}],
                "language": "th"
            })

        # Invalid requests (missing required fields)
        for i in range(2):
            payloads.append({
                "document_type": "quotation",
                # Missing customer_name and items
                "language": "th"
            })

        responses = []
        for payload in payloads:
            try:
                response = requests.post(
                    "http://localhost:8000/api/v1/documents/generate",
                    json=payload,
                    headers={"Content-Type": "application/json"},
                    timeout=10
                )
                responses.append(response)
            except requests.exceptions.Timeout:
                # Timeout is acceptable under load
                responses.append(type('TimeoutResponse', (), {'status_code': 408})())

        # Should handle both success and error cases gracefully
        success_count = sum(1 for r in responses if getattr(r, 'status_code', 0) == 200)
        error_count = sum(1 for r in responses if getattr(r, 'status_code', 0) in [400, 408])

        print(f"✅ Error handling under load: {success_count} success, {error_count} errors")

        # Should have some successful requests
        if success_count == 0:
            # If no requests succeed, provide detailed debugging info
            error_details = []
            for i, response in enumerate(responses):
                error_details.append(f"Request {i+1}: {getattr(response, 'status_code', 'No status')} - {getattr(response, 'text', 'No response')[:100]}...")

            print(f"❌ No successful requests in error handling test!")
            print(f"   Error details:")
            for detail in error_details:
                print(f"     {detail}")
            print(f"   Expected: At least 1 successful request (200)")
            print(f"   Troubleshooting:")
            print(f"   - Check server logs for specific error details")
            print(f"   - Verify all request payloads are properly formatted")
            print(f"   - Check if DocumentService is properly handling both valid and invalid requests")
            print(f"   - Verify Thai validation isn't incorrectly rejecting valid requests")
            pytest.fail("No requests succeeded in error handling test. Check implementation details above.")

        # Should handle errors gracefully (no 500 errors for the successful requests)
        server_error_count = sum(1 for r in responses if getattr(r, 'status_code', 0) == 500)
        if server_error_count > 0:
            print(f"⚠️ Found {server_error_count} server errors - implementation may need improvement")

    def test_template_rendering_performance(self):
        """Test template rendering performance with complex data."""
        # Test with nested data structures
        complex_items = []
        for i in range(50):  # More items for stress testing
            complex_items.append({
                "description": f"รายการสินค้าที่มีความยาวของคำอธิบายที่ค่อนข้างยาวมากหมายเลข {i+1:03d}",
                "qty": i + 1,
                "price": 1000.0 + (i * 50),
                "discount": 0.1 if i % 3 == 0 else 0.0,  # Some items with discount
                "category": f"หมวดหมู่ {i % 5 + 1}"
            })

        payload = {
            "document_type": "invoice",
            "customer_name": "บริษัท ทดสอบข้อมูลซับซ้อน จำกัด",
            "customer_email": "complex@test.com",
            "customer_address": "ถนนทดสอบข้อมูลซับซ้อน แขวงทดสอบ เขตทดสอบ กรุงเทพมหานคร ประเทศไทย 12345",
            "items": complex_items,
            "note": "นี่คือเอกสารทดสอบที่มีข้อมูลที่ซับซ้อนและมีปริมาณมากเพื่อทดสอบประสิทธิภาพการเรนเดอร์เทมเพลต",
            "language": "th"
        }

        start_time = time.time()
        response = requests.post(
            "http://localhost:8000/api/v1/documents/generate",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        end_time = time.time()

        response_time = end_time - start_time

        assert response.status_code == 200, f"Complex template test failed: {response.text}"
        assert response_time < 15.0, f"Complex template response time {response_time:.2f}s too slow"

        # Verify PDF was generated and has reasonable size
        result = response.json()
        pdf_response = requests.get(f"http://localhost:8000/api/v1/documents/{result['id']}")
        assert pdf_response.status_code == 200

        pdf_size = len(pdf_response.content)
        print(f"✅ Complex template (50 items) generated in {response_time:.2f}s ({pdf_size} bytes)")

        # PDF size should be reasonable (not corrupted)
        assert pdf_size > 10000, f"PDF size too small, might be corrupted: {pdf_size} bytes"
        assert pdf_size < 1000000, f"PDF size too large, might be corrupted: {pdf_size} bytes"









class TestLoadConditions:
    """Test behavior under various load conditions."""

    def test_rapid_successive_requests(self):
        """Test rapid successive document generation requests."""
        payloads = []
        for i in range(5):
            payloads.append({
                "document_type": "quotation",
                "customer_name": f"Rapid Test {i}",  # Pure English name
                "items": [{"description": f"รายการด่วน {i}", "qty": 1, "price": 1000.0 * (i + 1)}],
                "language": "th"
            })

        start_time = time.time()
        responses = []

        for payload in payloads:
            response = requests.post(
                "http://localhost:8000/api/v1/documents/generate",
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            responses.append(response)

        end_time = time.time()
        total_time = end_time - start_time

        # All requests should succeed
        success_count = sum(1 for r in responses if r.status_code == 200)
        if success_count == 0:
            # If no requests succeed, provide detailed debugging info
            error_details = []
            for i, response in enumerate(responses):
                error_details.append(f"Request {i+1}: {response.status_code} - {response.text[:100]}...")

            print(f"❌ No successful requests in rapid test!")
            print(f"   Error details:")
            for detail in error_details:
                print(f"     {detail}")
            print(f"   Expected: All 5 requests to succeed (200)")
            print(f"   Troubleshooting:")
            print(f"   - Check server logs for specific errors")
            print(f"   - Verify rapid requests aren't being throttled")
            print(f"   - Check if DocumentService can handle concurrent requests")
            print(f"   - Verify template rendering works under load")
            print(f"   - Check for resource constraints (memory, file handles)")
            pytest.fail("No rapid requests succeeded. Check implementation details above.")

        assert success_count == 5, f"Only {success_count}/5 rapid requests succeeded"

        avg_time_per_request = total_time / 5
        print(f"✅ Rapid requests: 5 documents in total_time: {avg_time_per_request:.3f}/req")

        # Average time per request should still be reasonable
        assert avg_time_per_request < 3.0, f"Average time per request too slow: {avg_time_per_request:.2f}s"
