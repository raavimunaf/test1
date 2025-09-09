#!/usr/bin/env python3
"""
Bulk Data Generator for Migration Testing
Generates realistic employee data for testing bulk migration performance
"""

import random
import string
import time
from datetime import datetime, timedelta
from typing import List, Dict, Generator
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class BulkDataGenerator:
    """Generates bulk employee data for migration testing"""
    
    def __init__(self, total_records: int = 10000000):  # 1 crore = 10 million
        self.total_records = total_records
        self.batch_size = 10000  # Generate in batches for memory efficiency
        
        # Sample data pools for realistic generation
        self.first_names = [
            "Aarav", "Aditi", "Arjun", "Avni", "Dev", "Diya", "Ishaan", "Kavya",
            "Krishna", "Mira", "Neha", "Rahul", "Riya", "Rohan", "Sanya", "Vivaan",
            "Zara", "Aisha", "Arnav", "Ira", "Kabir", "Kiara", "Lakshay", "Maya",
            "Nikhil", "Pari", "Rudra", "Sia", "Tanish", "Vanya", "Yash", "Zoya"
        ]
        
        self.last_names = [
            "Sharma", "Verma", "Patel", "Singh", "Kumar", "Gupta", "Chopra", "Malhotra",
            "Kapoor", "Joshi", "Reddy", "Kaur", "Nair", "Menon", "Iyer", "Pillai",
            "Bhat", "Rao", "Mehta", "Chauhan", "Yadav", "Jain", "Tiwari", "Mishra",
            "Dubey", "Saxena", "Sinha", "Choudhury", "Banerjee", "Mukherjee", "Das", "Roy"
        ]
        
        self.departments = [
            "Engineering", "Sales", "Marketing", "HR", "Finance", "Operations", 
            "Customer Support", "Product Management", "Research & Development",
            "Legal", "IT Support", "Quality Assurance", "Business Development",
            "Data Science", "Design", "Content", "Analytics", "Strategy"
        ]
        
        self.job_titles = [
            "Software Engineer", "Senior Developer", "Team Lead", "Manager",
            "Director", "VP", "CEO", "CTO", "CFO", "Analyst", "Specialist",
            "Coordinator", "Associate", "Consultant", "Architect", "Designer",
            "Researcher", "Writer", "Editor", "Trainer", "Recruiter", "Accountant"
        ]
        
        self.cities = [
            "Mumbai", "Delhi", "Bangalore", "Hyderabad", "Chennai", "Kolkata",
            "Pune", "Ahmedabad", "Jaipur", "Surat", "Lucknow", "Kanpur",
            "Nagpur", "Indore", "Thane", "Bhopal", "Visakhapatnam", "Pimpri",
            "Patna", "Vadodara", "Ghaziabad", "Ludhiana", "Agra", "Nashik"
        ]
        
        self.states = [
            "Maharashtra", "Delhi", "Karnataka", "Telangana", "Tamil Nadu",
            "West Bengal", "Gujarat", "Rajasthan", "Uttar Pradesh", "Madhya Pradesh",
            "Andhra Pradesh", "Bihar", "Punjab", "Haryana", "Jharkhand",
            "Chhattisgarh", "Odisha", "Assam", "Kerala", "Uttarakhand"
        ]

    def generate_employee_id(self, index: int) -> str:
        """Generate unique employee ID"""
        return f"EMP{index:08d}"
    
    def generate_email(self, first_name: str, last_name: str, index: int) -> str:
        """Generate realistic email address"""
        domain = random.choice(["company.com", "techcorp.in", "enterprise.org", "business.net"])
        return f"{first_name.lower()}.{last_name.lower()}{index % 1000}@{domain}"
    
    def generate_phone(self) -> str:
        """Generate realistic Indian phone number"""
        prefixes = ["6", "7", "8", "9"]
        prefix = random.choice(prefixes)
        remaining = ''.join(random.choices(string.digits, k=9))
        return f"+91{prefix}{remaining}"
    
    def generate_salary(self, experience_years: int, department: str) -> float:
        """Generate realistic salary based on experience and department"""
        base_salary = 30000  # Base salary in INR
        
        # Experience multiplier
        exp_multiplier = 1 + (experience_years * 0.15)
        
        # Department multiplier
        dept_multipliers = {
            "Engineering": 1.3,
            "Data Science": 1.4,
            "Product Management": 1.25,
            "Sales": 1.2,
            "Marketing": 1.1,
            "HR": 1.0,
            "Finance": 1.15,
            "Operations": 1.05
        }
        dept_multiplier = dept_multipliers.get(department, 1.0)
        
        # Add some randomness
        random_factor = random.uniform(0.8, 1.2)
        
        return round(base_salary * exp_multiplier * dept_multiplier * random_factor, 2)
    
    def generate_hire_date(self, experience_years: int) -> str:
        """Generate hire date based on experience"""
        current_date = datetime.now()
        hire_date = current_date - timedelta(days=experience_years * 365 + random.randint(0, 365))
        return hire_date.strftime("%Y-%m-%d")
    
    def generate_single_employee(self, index: int) -> Dict:
        """Generate a single employee record"""
        first_name = random.choice(self.first_names)
        last_name = random.choice(self.last_names)
        department = random.choice(self.departments)
        job_title = random.choice(self.job_titles)
        experience_years = random.randint(0, 25)
        city = random.choice(self.cities)
        state = random.choice(self.states)
        
        return {
            'employee_id': self.generate_employee_id(index),
            'first_name': first_name,
            'last_name': last_name,
            'email': self.generate_email(first_name, last_name, index),
            'phone': self.generate_phone(),
            'department': department,
            'job_title': job_title,
            'salary': self.generate_salary(experience_years, department),
            'hire_date': self.generate_hire_date(experience_years),
            'experience_years': experience_years,
            'city': city,
            'state': state,
            'is_active': random.choice([True, False]),
            'created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'updated_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    
    def generate_batch(self, start_index: int, batch_size: int) -> List[Dict]:
        """Generate a batch of employee records"""
        batch = []
        for i in range(batch_size):
            if start_index + i >= self.total_records:
                break
            batch.append(self.generate_single_employee(start_index + i))
        return batch
    
    def generate_all_data(self) -> Generator[List[Dict], None, None]:
        """Generate all data in batches"""
        logger.info(f"Starting generation of {self.total_records:,} records in batches of {self.batch_size:,}")
        
        for batch_start in range(0, self.total_records, self.batch_size):
            batch = self.generate_batch(batch_start, self.batch_size)
            logger.info(f"Generated batch {batch_start // self.batch_size + 1}: {len(batch):,} records")
            yield batch
    
    def generate_sample_data(self, sample_size: int = 1000) -> List[Dict]:
        """Generate a small sample for testing"""
        logger.info(f"Generating sample of {sample_size:,} records")
        return self.generate_batch(0, sample_size)
    
    def save_to_file(self, filename: str, data: List[Dict], format_type: str = 'csv'):
        """Save generated data to file"""
        if format_type.lower() == 'csv':
            self._save_to_csv(filename, data)
        elif format_type.lower() == 'json':
            self._save_to_json(filename, data)
        else:
            raise ValueError("Unsupported format. Use 'csv' or 'json'")
    
    def _save_to_csv(self, filename: str, data: List[Dict]):
        """Save data to CSV file"""
        import csv
        
        if not data:
            return
        
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = data[0].keys()
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for row in data:
                writer.writerow(row)
        
        logger.info(f"Saved {len(data):,} records to {filename}")
    
    def _save_to_json(self, filename: str, data: List[Dict]):
        """Save data to JSON file"""
        import json
        
        with open(filename, 'w', encoding='utf-8') as jsonfile:
            json.dump(data, jsonfile, indent=2, ensure_ascii=False)
        
        logger.info(f"Saved {len(data):,} records to {filename}")

def main():
    """Main function to demonstrate bulk data generation"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate bulk employee data for migration testing')
    parser.add_argument('--total', type=int, default=10000000, help='Total number of records to generate (default: 10M)')
    parser.add_argument('--batch-size', type=int, default=10000, help='Batch size for generation (default: 10000)')
    parser.add_argument('--sample', type=int, default=1000, help='Generate only a sample of records for testing')
    parser.add_argument('--output', type=str, default='bulk_employees.csv', help='Output filename')
    parser.add_argument('--format', choices=['csv', 'json'], default='csv', help='Output format')
    
    args = parser.parse_args()
    
    # Initialize generator
    generator = BulkDataGenerator(args.total)
    generator.batch_size = args.batch_size
    
    start_time = time.time()
    
    if args.sample:
        # Generate sample data
        sample_data = generator.generate_sample_data(args.sample)
        generator.save_to_file(args.output, sample_data, args.format)
    else:
        # Generate full dataset
        all_data = []
        for batch in generator.generate_all_data():
            all_data.extend(batch)
        
        generator.save_to_file(args.output, all_data, args.format)
    
    end_time = time.time()
    duration = end_time - start_time
    
    logger.info(f"Data generation completed in {duration:.2f} seconds")
    logger.info(f"Generated {args.total:,} records")
    logger.info(f"Average speed: {args.total / duration:,.0f} records/second")

if __name__ == "__main__":
    main()
