# Conversational Analytics Platform

## 1. Project Overview

The Conversational Analytics Platform is an AI-powered Business Intelligence application that allows users to analyze business and sales data using natural language.

Instead of writing SQL queries or manually creating reports, users can ask questions in simple language, such as:

* "What are the total sales?"
* "Which city has the highest sales?"
* "Show me the monthly sales trend."
* "What are the top 5 products by sales?"

The system will use Google Gemini to understand the user's question and convert it into structured information. The backend will then use this information to query the business data stored in Google Firebase Firestore.

After processing the data, the system will return the appropriate result to the user through the React frontend. Depending on the question, the result may be displayed as a KPI, table, bar chart, line chart, pie chart, or other suitable visualization.

### High-Level Workflow

User Question
↓
React Frontend
↓
Gemini AI
↓
Structured Query Information
↓
FastAPI Backend
↓
Firestore Database
↓
Data Filtering & Analytics
↓
Response
↓
React Visualization
↓
User

## Main Purpose

The main purpose of the platform is to make business data analysis easier and more accessible for users who do not have SQL or programming knowledge.

## 2. Problem Statement

Businesses generate a large amount of sales and operational data, but analyzing this data can be difficult for users who do not have technical knowledge.

Traditional business intelligence systems often require users to understand databases, SQL queries, spreadsheets, dashboards, or predefined reports. This can make it difficult and time-consuming for non-technical users to quickly obtain the information they need.

For example, a business manager may want to know:

* Which city generated the highest sales?
* Which products are performing best?
* What is the monthly sales trend?
* Which category generated the highest profit?

Without a conversational analytics system, answering these questions may require manually filtering data, writing database queries, or depending on a technical person or analyst.

The Conversational Analytics Platform aims to solve this problem by allowing users to ask business questions in natural language. The system will interpret the question using AI, retrieve the relevant data from the database, perform the required analysis, and present the result in an easy-to-understand format such as a KPI, table, or chart.

### Problem to be Solved

The core problem is:

> Non-technical business users need a simple way to ask questions about their business data and receive accurate, data-driven analytical answers without manually writing database queries or creating reports.

## 3. Project Objective

The primary objective of the Conversational Analytics Platform is to provide a simple, AI-powered interface through which non-technical users can analyze business and sales data using natural language.

The system aims to:

1. Allow users to ask business analytics questions in natural language without requiring SQL or programming knowledge.

2. Use Google Gemini to understand the user's question and convert it into structured query information.

3. Retrieve relevant business data from Google Firebase Firestore based on the interpreted query.

4. Perform accurate data filtering, aggregation, comparison, and other required analytical operations.

5. Present analytical results in an easy-to-understand format, including KPI values, tables, and suitable charts.

6. Reduce the time and technical effort required to obtain useful business insights from stored data.

7. Prevent the system from generating unsupported business results when the requested information is not available in the database.

### Primary Goal

The primary goal is to build a reliable conversational business intelligence system that transforms natural-language business questions into accurate, data-driven insights.

## 4. Target Users

The Conversational Analytics Platform is primarily designed for users who need to analyze business and sales data but may not have advanced technical or database knowledge.

### Primary Users

#### 4.1 Business Managers

Business managers can use the system to obtain quick insights into sales, profit, products, categories, and geographical performance.

Example questions:

* "What are the total sales?"
* "Which city has the highest sales?"
* "Which category is most profitable?"

#### 4.2 Sales Managers

Sales managers can use the platform to monitor sales performance, identify high-performing products or locations, and analyze sales trends over time.

#### 4.3 Business Analysts

Business analysts can use natural-language queries to explore business data and quickly obtain analytical results without manually creating every query or visualization.

#### 4.4 Store or Branch Managers

Store and branch managers can use the system to understand the performance of their relevant locations, products, and sales activities.

### User Technical Requirements

Users should not be required to have:

* SQL knowledge
* Database query-writing skills
* Programming knowledge
* Advanced data visualization skills

The platform should allow users to interact with business data through simple natural-language questions.

### Primary User Goal

The primary goal of the target users is to obtain useful and understandable business insights quickly by asking questions in natural language.

## 5. Functional Requirements

The Conversational Analytics Platform shall provide the following core functionalities.

### 5.1 Natural Language Query Input

The system shall allow users to enter business and sales-related questions using natural language.

Example:

> "Which city generated the highest sales?"

Users should not be required to write SQL queries.

### 5.2 AI-Based Question Understanding

The system shall use Google Gemini to understand the user's natural-language question and identify the required analytical information, such as:

* Metric
* City or geographical location
* Product
* Category
* Date or date range
* Aggregation type
* Grouping or comparison requirements

### 5.3 Structured Query Generation

The AI engine shall convert the interpreted question into a structured format that can be processed by the backend.

Example:

```json
{
  "metric": "sales",
  "city": "New York",
  "aggregation": "sum"
}
```

### 5.4 AI Output Validation

The backend shall validate the structured information generated by the AI before using it to query the database.

Invalid, incomplete, or unsupported query information shall not be directly executed.

### 5.5 Database Query

The backend shall use the validated query information to retrieve relevant business data from Google Firebase Firestore.

### 5.6 Data Filtering

The system shall support filtering business data according to relevant query parameters, such as:

* Date
* City
* Region
* Product
* Category
* Other supported dataset fields

### 5.7 Data Analytics

The system shall perform analytical operations on the retrieved data, including supported operations such as:

* Sum
* Average
* Count
* Minimum
* Maximum
* Ranking
* Grouping
* Comparison
* Trend analysis

### 5.8 Result Generation

The backend shall generate a structured response containing the analytical result and the information required by the frontend to display it.

### 5.9 Dynamic Visualization

The frontend shall display the result using an appropriate visualization based on the type of query.

Supported result formats may include:

* KPI cards
* Data tables
* Bar charts
* Line charts
* Pie charts
* Scatter plots

### 5.10 No-Data Handling

If the requested information does not exist in the database, the system shall return an appropriate message instead of generating or inventing business data.

Example:

> "No data found for the requested criteria."

### 5.11 Invalid or Unsupported Query Handling

If a user asks a question that is not supported by the platform, the system shall provide a clear response indicating that the request is outside the supported analytics scope.

### 5.12 Frontend and Backend Communication

The React frontend shall communicate with the FastAPI backend through defined API endpoints to send user queries and receive analytical results.

## 6. Non-Functional Requirements

The Conversational Analytics Platform should satisfy the following quality and operational requirements.

### 6.1 Accuracy

The system should provide analytical results based on the actual data available in the database.

The AI should not invent sales, profit, product, or other business values.

### 6.2 Reliability

The system should handle valid user queries consistently and provide predictable results for the same data and query conditions.

### 6.3 Performance

The system should process normal user queries within a reasonable response time.

Database queries and data processing should be designed to avoid unnecessary operations.

### 6.4 Security

Sensitive information such as API keys, Firebase credentials, and environment variables must not be exposed in the source code or committed to the Git repository.

Secrets should be stored using environment variables or other appropriate secure configuration methods.

### 6.5 Usability

The platform should be simple enough for non-technical business users to interact with without requiring SQL or programming knowledge.

Results should be presented in a clear and understandable format.

### 6.6 Maintainability

The backend and frontend should be organized into separate modules and services so that individual components can be updated or replaced without unnecessarily affecting the entire application.

### 6.7 Scalability

The system architecture should allow additional analytics operations, data fields, visualizations, and supported query types to be added in the future.

### 6.8 Error Handling

The system should handle invalid queries, missing data, AI errors, database errors, and API failures gracefully.

Users should receive understandable error messages rather than technical errors or application crashes.

### 6.9 Data Integrity

The system should preserve the correctness of business data during data import, storage, filtering, and analytical processing.

### 6.10 Compatibility

The frontend should run in modern web browsers, and the backend should operate in the supported Python environment defined by the project.

## 7. Supported Questions

The Conversational Analytics Platform shall support natural-language questions related to the business and sales data available in the database.

The exact values, locations, products, and categories supported by the system will depend on the selected dataset.

### 7.1 Sales and KPI Questions

Users can ask questions about basic business metrics, such as:

* "What are the total sales?"
* "What is the total profit?"
* "How many orders are there?"
* "What is the average sales value?"
* "What is the highest sales value?"
* "What is the lowest sales value?"

### 7.2 Product Questions

Users can ask questions related to products, including:

* "Which product has the highest sales?"
* "What are the top 5 products by sales?"
* "Which products generated the highest profit?"
* "Show sales for a specific product."

### 7.3 Category Questions

Users can ask questions about product categories and sub-categories, such as:

* "Which category has the highest sales?"
* "Which category generated the most profit?"
* "Show sales by category."
* "Compare sales between categories."

### 7.4 Geographical Questions

Users can ask questions about supported geographical fields in the dataset, such as:

* "Which city has the highest sales?"
* "Show sales by region."
* "Which region generated the most profit?"
* "Compare sales between two cities."

### 7.5 Date and Time Questions

Users can ask questions related to supported dates and time periods, such as:

* "What were the sales last month?"
* "Show monthly sales."
* "Which month had the highest sales?"
* "Show the sales trend over time."
* "Compare sales between two time periods."

### 7.6 Comparison Questions

The system should support comparisons between supported business dimensions, such as:

* City vs. city
* Category vs. category
* Product vs. product
* Region vs. region
* Time period vs. time period

Example:

> "Compare sales between New York and Los Angeles."

### 7.7 Ranking Questions

Users can request rankings of supported business entities.

Examples:

* "Show the top 5 products by sales."
* "Show the top 10 cities by profit."
* "Which category ranks first in sales?"

### 7.8 Combined Questions

The system should support questions containing multiple filters or conditions when the required data is available.

Example:

> "Show sales for Technology products in New York during 2024."

The system should identify the relevant filters and analytical operation before retrieving and processing the data.

### 7.9 Visualization-Oriented Questions

Users may request information that naturally requires a visual representation.

Examples:

* "Show monthly sales as a chart."
* "Show sales by category."
* "Show the sales trend over time."

The system should select an appropriate visualization based on the requested analysis and response type.

### 7.10 Dataset Dependency

Supported questions are dependent on the fields available in the selected dataset.

For example, if the dataset does not contain a particular field such as customer age, the system shall not claim to provide customer-age analysis.

The system should only answer questions that can be supported by the available business data.

## 8. Expected Responses

The system shall return analytical results in a structured format that can be displayed clearly by the frontend.

The response format should depend on the type of question and the type of analysis performed.

### 8.1 KPI Response

For questions requesting a single business metric, the system should return a KPI-style result.

Examples:

* Total Sales
* Total Profit
* Total Orders
* Average Sales

Example:

> "What are the total sales?"

Expected display:

```text
Total Sales
$250,000
```

### 8.2 Table Response

For questions requiring detailed records or multiple values, the system should return a tabular response.

Example:

> "Show the top 5 products by sales."

Expected display:

| Product   |   Sales |
| --------- | ------: |
| Product A | $50,000 |
| Product B | $42,000 |
| Product C | $38,000 |
| Product D | $35,000 |
| Product E | $31,000 |

### 8.3 Bar Chart Response

Bar charts should be used when comparing values across categories or entities.

Examples:

* Sales by city
* Sales by category
* Profit by region
* Top products by sales

Example:

> "Show sales by category."

Expected visualization:

```text
Category A  ██████████
Category B  ███████
Category C  █████
```

### 8.4 Line Chart Response

Line charts should be used for trends and values changing over time.

Examples:

* Monthly sales
* Monthly profit
* Yearly sales trend

Example:

> "Show monthly sales trend."

Expected visualization:

```text
Sales
  │       ╭──╮
  │   ╭───╯  ╰──╮
  │───╯         ╰──
  └────────────────
      Jan Feb Mar Apr
```

### 8.5 Pie Chart Response

Pie charts may be used to show the proportional distribution of a metric across categories.

Examples:

* Sales share by category
* Profit share by region

Example:

> "Show the percentage of sales by category."

### 8.6 Scatter Plot Response

Scatter plots may be used when the analysis requires understanding the relationship between two numerical variables.

Example:

> "Show the relationship between sales and profit."

### 8.7 Ranking Response

For ranking questions, the system should return ordered results, preferably using a table or bar chart.

Example:

> "What are the top 5 cities by sales?"

The result should be ordered from highest to lowest.

### 8.8 Comparison Response

For comparison questions, the system should clearly show the values being compared.

Example:

> "Compare sales between New York and Los Angeles."

Expected result:

```text
New York        $120,000
Los Angeles     $95,000
```

A suitable chart may also be displayed.

### 8.9 No-Data Response

If no matching data is available, the system should return a clear message.

Example:

> "No data found for the requested criteria."

The system must not create or guess a result.

### 8.10 Error Response

If the request cannot be processed because of an invalid query, unsupported request, AI failure, database failure, or other system error, the frontend should display a user-friendly error message.

Technical error details should not be unnecessarily exposed to the end user.

### 8.11 Structured Backend Response

The backend should return a consistent structured response so that the React frontend can determine how to render the result.

A conceptual response may contain information such as:

```json
{
  "type": "bar_chart",
  "title": "Sales by Category",
  "data": []
}
```

The exact response schema will be finalized during the backend and API design phases.

## 9. Out of Scope

The following functionalities are outside the current scope of the Conversational Analytics Platform.

### 9.1 General-Purpose Chatbot

The system is not intended to function as a general-purpose conversational AI assistant.

It will focus specifically on business and sales analytics based on the available dataset.

### 9.2 General Internet Search

The system will not provide general web search functionality or retrieve unrelated information such as news, weather, entertainment, or general internet content.

### 9.3 Medical or Legal Advice

The platform will not be designed to provide medical, legal, financial-advisory, or other professional advice.

### 9.4 Coding Assistant

The system will not function as a programming or coding assistant.

Questions unrelated to the supported business analytics scope should not be processed as business queries.

### 9.5 Automatic Business Data Generation

The system shall not invent, assume, or fabricate business data when the requested information is not available in the database.

### 9.6 Unsupported Dataset Analysis

The system will not analyze fields or information that do not exist in the selected dataset.

For example, if the dataset does not contain customer age, the system will not provide customer-age analytics.

### 9.7 Advanced Predictive Analytics

Advanced machine-learning forecasting, predictive modeling, recommendation systems, and complex statistical analysis are outside the initial project scope unless explicitly added as future enhancements.

### 9.8 Real-Time External Business Systems

The initial system will not automatically connect to external enterprise systems such as live POS, ERP, CRM, or accounting platforms.

The initial implementation will work with the project's selected and prepared dataset stored in Firestore.

### 9.9 Multi-Tenant Enterprise Management

Advanced enterprise features such as organization management, complex role-based access control, subscription management, billing, and multi-tenant account management are outside the initial scope.

### 9.10 Mobile Application

The initial project will be implemented as a web-based application. A dedicated native Android or iOS application is outside the current scope.

### Scope Boundary

The platform's primary responsibility is:

> Natural-language business questions → AI interpretation → database-based analytics → understandable analytical results.

Features outside this workflow will not be considered part of the initial implementation.

## 10. System Rules

The Conversational Analytics Platform shall follow the following rules to ensure accuracy, reliability, security, and predictable behavior.

### 10.1 Data-Driven Answers

All business and sales answers must be based on data available in the application's database.

The system must not invent business values.

### 10.2 No Unsupported Assumptions

The system must not assume values that are not provided by the user or available in the dataset.

For example, if a user does not specify a location and the question requires a location filter, the system should not randomly select a location.

### 10.3 AI Output Must Be Validated

AI-generated structured query information must be validated by the backend before being used for database operations.

The system must not blindly trust AI-generated output.

### 10.4 Database Is the Source of Business Data

Firestore will act as the source of stored business data for the application's analytics operations.

Gemini will interpret the user's question, but it will not be treated as the source of the business data.

### 10.5 Only Supported Fields Can Be Queried

The system may only query fields that are defined and supported by the selected dataset and application schema.

### 10.6 No Data Means No Fabricated Result

If the database contains no matching records, the system must return an appropriate no-data response instead of generating an estimated or fabricated result.

### 10.7 Clear Error Handling

If a request cannot be processed, the system should provide a clear and user-friendly error message.

The application should not expose unnecessary internal technical details to the user.

### 10.8 Secure Secrets

API keys, Firebase credentials, database credentials, and other sensitive configuration values must not be hardcoded into application source code or committed to the Git repository.

Sensitive configuration should be managed through environment variables or appropriate secure configuration methods.

### 10.9 Scope Enforcement

The system should only process questions that fall within the supported business analytics scope.

Unrelated or unsupported requests should receive an appropriate response.

### 10.10 Consistent Response Structure

Backend responses should follow a defined and consistent structure so that the frontend can reliably determine how to display the result.

### 10.11 Accuracy Before Visualization

The system must calculate and validate the analytical result before displaying it as a chart, table, or KPI.

Visualization must represent the actual calculated result and must not modify the underlying values.

### 10.12 Dataset Dependency

The behavior and capabilities of the analytics system depend on the fields and records available in the selected dataset.

Any supported-question list, database schema, and analytical functionality must remain consistent with the actual dataset.

## 11. Phase 1 Acceptance Criteria

Phase 1 shall be considered complete when the project's initial requirements and scope have been clearly defined and documented.

The following criteria must be satisfied:

* [ ] The project's purpose and overall workflow are clearly documented.
* [ ] The main problem being solved is clearly defined.
* [ ] The primary project objectives are documented.
* [ ] Target users have been identified.
* [ ] Core functional requirements have been defined.
* [ ] Non-functional requirements such as accuracy, security, reliability, usability, and maintainability have been documented.
* [ ] Supported business and sales question types have been identified.
* [ ] Expected response formats and visualizations have been defined.
* [ ] Features outside the current project scope have been documented.
* [ ] Core system rules have been defined.
* [ ] The requirements document is consistent with the intended project architecture and workflow.

### Phase 1 Completion Statement

Phase 1 is complete when the above requirements have been reviewed and approved as the foundation for the subsequent database schema, dataset, backend, AI, and frontend implementation phases.
