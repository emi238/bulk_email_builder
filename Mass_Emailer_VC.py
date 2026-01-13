import pandas as pd

while True:
    # Define the columns needed for the email processing
    required_columns = ['Name', 'Contact', 'Contact Email', 'Tailored Paragraph']
    
    # Ask user for excel filepath
    filepath = input("Filepath to the investor list (excel): ")
    sheet = input("Sheet Name to Action: ")
    
    df = pd.read_excel(filepath, sheet_name=sheet, skiprows=2)
    df = df[required_columns]
    
    print(df)
    
    # Collect all templates
    subject_template = input("Enter email subject (use [Investor_Institution] for VC name): ")
    salutation_template = input("Enter salutation (use [Investor] for VC name): ")
    main_body_template = input("Enter main body (use [Investor_Institution] for institution): ")
    cta_template = input("Enter call-to-action template: ")
    
    # Format function for main body
    def format_body_paragraph(text):
        formatted = ""
        for i in range(len(text)):
            if text[i] == '.' and i+1 < len(text) and text[i+1] != ' ':
                formatted += '.\n\n'
            else:
                formatted += text[i]
        return formatted
    
    # Create complete emails
    complete_emails = []
    
    for index, row in df.iterrows():
        # Get data
        contact_name = str(row['Contact'])
        investor_institution = str(row['Name'])
        tailored_para = str(row['Tailored Paragraph'])
        
        # Extract first name
        first_name = contact_name.split()[0] if contact_name else ""
        
        # Build email components
        subject = subject_template.replace('[Investor_Institution]', investor_institution)
        salutation = salutation_template.replace('[Investor]', first_name)
        main_body = main_body_template.replace('[Investor_Institution]', investor_institution)
        main_body = format_body_paragraph(main_body)
        
        # Combine everything
        email_body = f"{salutation}\n\n{main_body}\n\n{tailored_para}\n\n{cta_template}"
        
        # Add to list
        complete_emails.append({
            'Contact': contact_name,
            'Email': str(row['Contact Email']),
            'Subject': subject,
            'Body': email_body
        })
    
    # Print all emails with basic formatting
    for i, email in enumerate(complete_emails):
        print(f"\nEmail #{i+1}:")
        print(f"To: {email['Email']}")
        print(f"Subject: {email['Subject']}")
        print(f"Body: {email['Body']}")
        print("-" * 30)
    
    print(f"\nTotal emails created: {len(complete_emails)}")
    
    # Ask if user wants to run another batch
    another_batch = input("\nDo you want to create another batch of emails? (yes/no): ").lower()
    if another_batch not in ['yes', 'y']:
        print("Goodbye!")
        break

