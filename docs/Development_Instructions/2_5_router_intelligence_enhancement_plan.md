# Phase 2.5: Router Intelligence Enhancement Plan

## 📊 Executive Summary

**Priority**: CRITICAL - Required for 90%+ test success rate  
**Current Issue**: Router fails to extract required fields from natural language  
**Target**: 95% field extraction accuracy  
**Estimated Effort**: 1-2 weeks  

## 🔍 Current Router Analysis

### Test Results Analysis
From end-to-end workflow tests, the router currently extracts:
```python
# Current extraction results (FAILED):
{
    'issuer': None,           # Required: "Global Finance Inc."
    'product_name': None,      # Required: "SP 500 Autocallable Note"
    'underlying_asset': None,  # Required: "S&P 500 Index"
    'currency': None,          # Required: "USD"
    'principal_amount': None,  # Required: 1000000.0
    'issue_date': None,        # Required: "2024-01-15"
    'maturity_date': None,     # Required: "2027-01-15"
    'target_audience': None,   # Required: "retail_investors"
    'risk_tolerance': None,    # Required: "medium"
    'investment_objective': None, # Required: "growth"
    'regulatory_jurisdiction': None, # Required: "US"
    'distribution_method': None # Required: "private_placement"
}
```

### Root Cause Analysis
1. **No Date Pattern Recognition**: Router cannot extract dates from natural language
2. **No Entity Recognition**: Router cannot identify financial entities and products
3. **No Context Inference**: Router cannot infer missing fields from product characteristics
4. **No Smart Defaults**: Router doesn't apply intelligent defaults for missing fields
5. **No Validation Feedback**: Router doesn't provide helpful error messages

## 🚀 Enhancement Implementation Plan

### Phase 2.5.1: Date Pattern Recognition (Week 1, Days 1-3)

#### 1.1 Date Extraction Implementation
```python
class DateExtractor:
    """Extract dates from natural language text"""
    
    def __init__(self):
        self.date_patterns = {
            'issue_date': [
                r'issue[d]?\s+(?:on\s+)?(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
                r'start(?:ing)?\s+(?:on\s+)?(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
                r'launch(?:ed)?\s+(?:on\s+)?(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
                r'effective\s+(?:date\s+)?(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
                r'begin(?:ning)?\s+(?:on\s+)?(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})'
            ],
            'maturity_date': [
                r'matur(?:ity|e)\s+(?:on\s+)?(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
                r'end(?:ing)?\s+(?:on\s+)?(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
                r'expir(?:y|es)\s+(?:on\s+)?(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
                r'term\s+of\s+(\d+)\s+(?:years?|months?)\s+from\s+(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
                r'(\d+)\s+(?:years?|months?)\s+term\s+from\s+(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})'
            ]
        }
    
    def extract_dates(self, text: str) -> Dict[str, str]:
        """Extract issue and maturity dates from text"""
        extracted_dates = {}
        
        for date_type, patterns in self.date_patterns.items():
            for pattern in patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                if matches:
                    if date_type == 'maturity_date' and len(matches[0]) == 2:
                        # Handle term-based maturity calculation
                        term, start_date = matches[0]
                        extracted_dates['issue_date'] = self._parse_date(start_date)
                        extracted_dates['maturity_date'] = self._calculate_maturity_date(
                            start_date, int(term)
                        )
                    else:
                        extracted_dates[date_type] = self._parse_date(matches[0])
                    break
        
        return extracted_dates
    
    def _parse_date(self, date_str: str) -> str:
        """Parse and standardize date format"""
        # Implementation for date parsing and standardization
        pass
    
    def _calculate_maturity_date(self, issue_date: str, term_years: int) -> str:
        """Calculate maturity date from issue date and term"""
        # Implementation for maturity date calculation
        pass
```

#### 1.2 Date Pattern Testing
```python
def test_date_extraction():
    """Test date extraction functionality"""
    test_cases = [
        {
            'input': 'Generate ISM document for SP 500 Autocallable Note issued on 2024-01-15 with 3 year term',
            'expected': {
                'issue_date': '2024-01-15',
                'maturity_date': '2027-01-15'
            }
        },
        {
            'input': 'Create ISM for Global Finance Inc. starting 01/15/2024, maturing 01/15/2027',
            'expected': {
                'issue_date': '2024-01-15',
                'maturity_date': '2027-01-15'
            }
        }
    ]
    
    extractor = DateExtractor()
    for test_case in test_cases:
        result = extractor.extract_dates(test_case['input'])
        assert result == test_case['expected']
```

### Phase 2.5.2: Entity Recognition (Week 1, Days 4-5)

#### 2.1 Financial Entity Extraction
```python
class EntityExtractor:
    """Extract financial entities from natural language text"""
    
    def __init__(self):
        self.entity_patterns = {
            'issuer': [
                r'issued\s+by\s+([A-Za-z\s&.,]+?)(?:\s+with|\s+for|\s+underlying|\s+currency)',
                r'issuer[:\s]+([A-Za-z\s&.,]+?)(?:\s+with|\s+for|\s+underlying|\s+currency)',
                r'([A-Za-z\s&.,]+?)\s+issued\s+',
                r'([A-Za-z\s&.,]+?)\s+as\s+issuer'
            ],
            'product_name': [
                r'([A-Za-z\s0-9]+?(?:Note|Bond|Security|Product|Series))',
                r'product[:\s]+([A-Za-z\s0-9]+?)(?:\s+with|\s+for|\s+underlying)',
                r'([A-Za-z\s0-9]+?)\s+(?:Autocallable|Barrier|Reverse)'
            ],
            'underlying_asset': [
                r'underlying[:\s]+([A-Za-z\s&.,]+?)(?:\s+with|\s+for|\s+currency)',
                r'index[:\s]+([A-Za-z\s&.,]+?)(?:\s+with|\s+for|\s+currency)',
                r'([A-Za-z\s&.,]+?)\s+Index',
                r'([A-Za-z\s&.,]+?)\s+as\s+underlying'
            ],
            'currency': [
                r'currency[:\s]+([A-Z]{3})',
                r'([A-Z]{3})\s+denominated',
                r'([A-Z]{3})\s+currency',
                r'([A-Z]{3})\s+principal'
            ],
            'principal_amount': [
                r'principal[:\s]+([0-9,]+(?:\.[0-9]+)?)\s*(?:million|thousand|k|m)?',
                r'amount[:\s]+([0-9,]+(?:\.[0-9]+)?)\s*(?:million|thousand|k|m)?',
                r'([0-9,]+(?:\.[0-9]+)?)\s*(?:million|thousand|k|m)?\s*(?:USD|EUR|GBP)',
                r'([0-9,]+(?:\.[0-9]+)?)\s*principal'
            ]
        }
    
    def extract_entities(self, text: str) -> Dict[str, Any]:
        """Extract financial entities from text"""
        extracted_entities = {}
        
        for entity_type, patterns in self.entity_patterns.items():
            for pattern in patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                if matches:
                    if entity_type == 'principal_amount':
                        extracted_entities[entity_type] = self._parse_amount(matches[0])
                    else:
                        extracted_entities[entity_type] = matches[0].strip()
                    break
        
        return extracted_entities
    
    def _parse_amount(self, amount_str: str) -> float:
        """Parse and convert amount string to float"""
        # Remove commas and convert to float
        clean_amount = amount_str.replace(',', '')
        
        # Handle multipliers (k, m, million, thousand)
        if 'million' in clean_amount.lower() or 'm' in clean_amount.lower():
            multiplier = 1000000
        elif 'thousand' in clean_amount.lower() or 'k' in clean_amount.lower():
            multiplier = 1000
        else:
            multiplier = 1
        
        # Extract numeric value
        numeric_value = re.findall(r'[0-9]+(?:\.[0-9]+)?', clean_amount)[0]
        return float(numeric_value) * multiplier
```

#### 2.2 Entity Recognition Testing
```python
def test_entity_extraction():
    """Test entity extraction functionality"""
    test_cases = [
        {
            'input': 'Generate ISM document for SP 500 Autocallable Note Series 2024-1 issued by Global Finance Inc. with underlying S&P 500 Index, USD 1,000,000 principal',
            'expected': {
                'issuer': 'Global Finance Inc.',
                'product_name': 'SP 500 Autocallable Note Series 2024-1',
                'underlying_asset': 'S&P 500 Index',
                'currency': 'USD',
                'principal_amount': 1000000.0
            }
        }
    ]
    
    extractor = EntityExtractor()
    for test_case in test_cases:
        result = extractor.extract_entities(test_case['input'])
        assert result == test_case['expected']
```

### Phase 2.5.3: Context Inference (Week 1, Days 6-7)

#### 3.1 Context-Based Field Inference
```python
class ContextInferrer:
    """Infer missing fields from context and product characteristics"""
    
    def __init__(self):
        self.context_patterns = {
            'target_audience': {
                'retail_investors': [
                    'retail', 'individual', 'personal', 'small investor',
                    'autocallable', 'structured note', 'principal protected'
                ],
                'institutional': [
                    'institutional', 'pension', 'endowment', 'fund',
                    'qualified', 'accredited', 'sophisticated'
                ],
                'accredited': [
                    'accredited', 'sophisticated', 'qualified',
                    'high net worth', 'professional'
                ]
            },
            'risk_tolerance': {
                'low': [
                    'conservative', 'preservation', 'stable', 'low risk',
                    'principal protected', 'guaranteed'
                ],
                'medium': [
                    'balanced', 'moderate', 'growth', 'autocallable',
                    'structured', 'enhanced return'
                ],
                'high': [
                    'aggressive', 'speculative', 'high risk',
                    'maximum return', 'leveraged'
                ]
            },
            'investment_objective': {
                'capital_preservation': [
                    'preserve', 'protect', 'safety', 'guaranteed',
                    'principal protected'
                ],
                'income_generation': [
                    'income', 'dividend', 'coupon', 'yield',
                    'interest', 'payment'
                ],
                'growth': [
                    'growth', 'appreciation', 'capital gains',
                    'enhanced return', 'upside'
                ],
                'diversification': [
                    'diversify', 'hedge', 'portfolio', 'risk management'
                ]
            },
            'regulatory_jurisdiction': {
                'US': [
                    'SEC', 'FINRA', 'United States', 'US', 'American',
                    'NYSE', 'NASDAQ'
                ],
                'Canada': [
                    'OSC', 'CSA', 'Canada', 'Canadian', 'TSX'
                ],
                'EU': [
                    'ESMA', 'European', 'EU', 'MiFID', 'Euro'
                ],
                'UK': [
                    'FCA', 'United Kingdom', 'UK', 'London', 'LSE'
                ]
            },
            'distribution_method': {
                'private_placement': [
                    'private', '144A', 'Reg D', 'accredited',
                    'sophisticated', 'qualified'
                ],
                'public_offering': [
                    'public', 'IPO', 'registered', 'retail'
                ],
                'institutional_only': [
                    'institutional', 'qualified', 'professional'
                ],
                'retail_distribution': [
                    'retail', 'broker', 'advisor', 'public'
                ]
            }
        }
    
    def infer_context(self, text: str, extracted_data: Dict[str, Any]) -> Dict[str, str]:
        """Infer missing fields from context"""
        inferred_context = {}
        
        for field_type, categories in self.context_patterns.items():
            if field_type not in extracted_data or extracted_data[field_type] is None:
                inferred_value = self._infer_field_from_context(text, categories)
                if inferred_value:
                    inferred_context[field_type] = inferred_value
        
        return inferred_context
    
    def _infer_field_from_context(self, text: str, categories: Dict[str, List[str]]) -> Optional[str]:
        """Infer field value from text context"""
        text_lower = text.lower()
        
        for category, keywords in categories.items():
            for keyword in keywords:
                if keyword.lower() in text_lower:
                    return category
        
        return None
```

### Phase 2.5.4: Smart Defaults (Week 2, Days 1-2)

#### 4.1 Intelligent Default Assignment
```python
class SmartDefaultAssigner:
    """Apply intelligent defaults for missing fields"""
    
    def __init__(self):
        self.defaults = {
            'target_audience': 'retail_investors',
            'risk_tolerance': 'medium',
            'investment_objective': 'growth',
            'regulatory_jurisdiction': 'US',
            'distribution_method': 'private_placement',
            'product_type': 'autocallable'
        }
    
    def apply_smart_defaults(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Apply intelligent defaults for missing fields"""
        enhanced_data = data.copy()
        
        # Apply basic defaults
        for field, default_value in self.defaults.items():
            if field not in enhanced_data or enhanced_data[field] is None:
                enhanced_data[field] = default_value
        
        # Apply context-aware defaults
        enhanced_data = self._apply_context_aware_defaults(enhanced_data)
        
        return enhanced_data
    
    def _apply_context_aware_defaults(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Apply defaults based on product characteristics"""
        
        # Infer risk tolerance from product type
        if 'product_type' in data:
            if 'autocallable' in data['product_type'].lower():
                data['risk_tolerance'] = 'medium'
            elif 'barrier' in data['product_type'].lower():
                data['risk_tolerance'] = 'high'
            elif 'principal protected' in data.get('product_name', '').lower():
                data['risk_tolerance'] = 'low'
        
        # Infer investment objective from product features
        if 'product_name' in data:
            if 'income' in data['product_name'].lower():
                data['investment_objective'] = 'income_generation'
            elif 'growth' in data['product_name'].lower():
                data['investment_objective'] = 'growth'
            elif 'protected' in data['product_name'].lower():
                data['investment_objective'] = 'capital_preservation'
        
        return data
```

### Phase 2.5.5: Enhanced Router Integration (Week 2, Days 3-5)

#### 5.1 Enhanced SmartAgentRouter
```python
class EnhancedSmartAgentRouter(SmartAgentRouter):
    """Enhanced router with intelligent information extraction"""
    
    def __init__(self):
        super().__init__()
        self.date_extractor = DateExtractor()
        self.entity_extractor = EntityExtractor()
        self.context_inferrer = ContextInferrer()
        self.default_assigner = SmartDefaultAssigner()
    
    def analyze_request(self, user_request: str) -> RoutingDecision:
        """Enhanced request analysis with comprehensive data extraction"""
        
        # Basic routing decision
        routing_decision = super().analyze_request(user_request)
        
        # Enhanced data extraction
        extracted_data = self._extract_comprehensive_data(user_request)
        
        # Apply smart defaults
        enhanced_data = self.default_assigner.apply_smart_defaults(extracted_data)
        
        # Validate and suggest improvements
        validation_result = self._validate_extracted_data(enhanced_data)
        
        # Update routing decision with enhanced data
        routing_decision.extracted_data = enhanced_data
        routing_decision.confidence_score = self._calculate_enhanced_confidence(validation_result)
        
        return routing_decision
    
    def _extract_comprehensive_data(self, text: str) -> Dict[str, Any]:
        """Extract all required fields from natural language"""
        extracted_data = {}
        
        # Extract dates
        extracted_data.update(self.date_extractor.extract_dates(text))
        
        # Extract entities
        extracted_data.update(self.entity_extractor.extract_entities(text))
        
        # Infer context
        context_data = self.context_inferrer.infer_context(text, extracted_data)
        extracted_data.update(context_data)
        
        return extracted_data
    
    def _validate_extracted_data(self, data: Dict[str, Any]) -> Dict[str, bool]:
        """Validate extracted data completeness"""
        required_fields = [
            'issuer', 'product_name', 'underlying_asset', 'currency',
            'principal_amount', 'issue_date', 'maturity_date',
            'target_audience', 'risk_tolerance', 'investment_objective',
            'regulatory_jurisdiction', 'distribution_method'
        ]
        
        validation_result = {}
        for field in required_fields:
            validation_result[field] = field in data and data[field] is not None
        
        return validation_result
    
    def _calculate_enhanced_confidence(self, validation_result: Dict[str, bool]) -> float:
        """Calculate confidence score based on data completeness"""
        total_fields = len(validation_result)
        valid_fields = sum(validation_result.values())
        return valid_fields / total_fields
```

## 📋 Implementation Timeline

### Week 1: Core Extraction
- **Days 1-3**: Date Pattern Recognition
- **Days 4-5**: Entity Recognition
- **Days 6-7**: Context Inference

### Week 2: Integration & Testing
- **Days 1-2**: Smart Defaults
- **Days 3-5**: Enhanced Router Integration
- **Day 5**: Comprehensive Testing

## 🎯 Success Metrics

### Target Improvements
- **Field Extraction Accuracy**: 0% → 95%+
- **Date Recognition**: 0% → 90%+
- **Entity Recognition**: 0% → 85%+
- **Context Inference**: 0% → 80%+
- **Overall Router Confidence**: 25% → 90%+

### Quality Metrics
- **Processing Time**: < 5 seconds for complex requests
- **Error Rate**: < 5% for field extraction
- **Coverage**: 100% of required fields extracted or defaulted
- **User Experience**: Clear error messages and suggestions

## 🧪 Testing Strategy

### Unit Tests
```python
def test_enhanced_router():
    """Test enhanced router functionality"""
    router = EnhancedSmartAgentRouter()
    
    test_request = """
    Generate ISM document for SP 500 Autocallable Note Series 2024-1 
    issued by Global Finance Inc. on 2024-01-15 with underlying S&P 500 Index, 
    USD 1,000,000 principal, 3 year term, targeting retail investors
    """
    
    result = router.analyze_request(test_request)
    
    # Validate extracted data
    assert result.extracted_data['issuer'] == 'Global Finance Inc.'
    assert result.extracted_data['product_name'] == 'SP 500 Autocallable Note Series 2024-1'
    assert result.extracted_data['underlying_asset'] == 'S&P 500 Index'
    assert result.extracted_data['currency'] == 'USD'
    assert result.extracted_data['principal_amount'] == 1000000.0
    assert result.extracted_data['issue_date'] == '2024-01-15'
    assert result.extracted_data['maturity_date'] == '2027-01-15'
    assert result.extracted_data['target_audience'] == 'retail_investors'
    assert result.confidence_score >= 0.9
```

### Integration Tests
```python
def test_router_integration():
    """Test router integration with GlobalAgent"""
    global_agent = GlobalAgent()
    
    test_request = "Generate ISM document for autocallable note"
    
    response = global_agent.process_request(test_request)
    
    # Validate that router provides sufficient data
    assert response.success or "validation" in response.error_message.lower()
    assert response.session_id is not None
```

## 🚀 Next Steps

1. **Immediate**: Implement DateExtractor class
2. **Week 1**: Complete EntityExtractor and ContextInferrer
3. **Week 2**: Implement SmartDefaultAssigner and EnhancedSmartAgentRouter
4. **Week 2**: Comprehensive testing and validation
5. **Week 3**: Integration with existing framework

## 📊 Expected Impact

After implementation, the router should:
- ✅ Extract dates from natural language (95% accuracy)
- ✅ Identify financial entities (85% accuracy)
- ✅ Infer missing fields from context (80% accuracy)
- ✅ Apply intelligent defaults for missing fields
- ✅ Provide clear error messages and suggestions
- ✅ Achieve 90%+ overall confidence score

This enhancement will directly address the 25% success rate in end-to-end workflow tests and enable the system to achieve 90%+ success rate.

**Priority**: CRITICAL - Required for production readiness  
**Effort**: 2 weeks of focused development  
**Risk**: Low - Well-defined scope and clear implementation path 