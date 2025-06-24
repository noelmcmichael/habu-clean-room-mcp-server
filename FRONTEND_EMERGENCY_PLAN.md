# 🚨 Frontend Emergency Debugging Plan

## 🎯 **Current Issues**
- Pages loading inconsistently or not at all
- 400 errors reported from multiple locations
- Performance worse than before optimization
- Cross-country user experiencing issues

## 📋 **Phase 1: Immediate Diagnostics (5 minutes)**

### **1.1 Check Current API Health**
- Test all critical endpoints for 400/500 errors
- Verify basic API functionality
- Check error patterns and frequency

### **1.2 Identify Error Sources** 
- CDN optimization code bugs?
- Redis connection failures causing cascading errors?
- New dependencies or imports causing issues?
- Response header conflicts?

### **1.3 Scope Assessment**
- Frontend only vs API issues
- Geographic distribution of problems
- Specific pages/endpoints affected

## 📋 **Phase 2: Quick Rollback Option (10 minutes)**

### **2.1 Prepare Clean Rollback**
- Create emergency branch with pre-CDN code
- Remove CDN optimization from critical paths
- Revert to stable lazy loading if needed

### **2.2 Rollback Triggers**
- If >50% of endpoints showing errors
- If core functionality broken
- If issues are widespread/systemic

## 📋 **Phase 3: Targeted Debugging (15 minutes)**

### **3.1 CDN Code Review**
- Check `cdn_optimization.py` for bugs
- Verify Flask response handling
- Look for race conditions or timeout issues

### **3.2 Frontend Code Review**
- Check removed lazy loading impacts
- Verify React component imports
- Look for TypeScript/build issues

### **3.3 API Integration Review**
- Check `apply_cdn_optimization()` calls
- Verify response object handling
- Look for JSON serialization issues

## 📋 **Phase 4: Incremental Fixes (20 minutes)**

### **4.1 Conservative CDN Approach**
- Disable CDN optimization on critical endpoints
- Keep only basic compression
- Remove complex headers temporarily

### **4.2 Frontend Stability**
- Revert to proven working state
- Add minimal necessary changes only
- Test each change individually

### **4.3 Gradual Re-enablement**
- Add optimizations one by one
- Test each addition thoroughly
- Monitor for error patterns

## 📋 **Phase 5: Verification & Monitoring (10 minutes)**

### **5.1 Multi-location Testing**
- Test from multiple geographic locations
- Verify consistent behavior
- Check for intermittent issues

### **5.2 Performance Baseline**
- Establish stable performance metrics
- Compare to pre-optimization state
- Ensure we haven't regressed

## 🚀 **Execution Plan**

### **STEP 1: Emergency Diagnostics**
```bash
# Test all critical endpoints
curl -I https://habu-demo-api-v2.onrender.com/
curl -I https://habu-demo-api-v2.onrender.com/health
curl -s https://habu-demo-api-v2.onrender.com/api/mcp/habu_list_partners
curl -s https://habu-demo-frontend-v2.onrender.com/

# Check for error patterns
curl -s https://habu-demo-api-v2.onrender.com/ | jq
```

### **STEP 2: CDN Code Analysis**
- Review `apply_cdn_optimization()` function
- Check Flask response object handling
- Look for serialization/header issues

### **STEP 3: Conservative Rollback**
- Create minimal CDN version
- Remove complex optimizations
- Keep only proven features

### **STEP 4: Frontend Stability**
- Revert problematic React changes
- Test page loading thoroughly
- Ensure consistent behavior

### **STEP 5: Gradual Recovery**
- Add back optimizations incrementally
- Test each addition
- Monitor for issues

## 🎯 **Success Criteria**
- ✅ No 400/500 errors across all endpoints
- ✅ Consistent page loading from multiple locations
- ✅ Performance equal to or better than pre-optimization
- ✅ Stable operation for 15+ minutes continuous testing

## 🚨 **Rollback Decision Tree**

### **Immediate Rollback If:**
- >3 consecutive 400/500 errors
- Core chat functionality broken
- Multiple users reporting issues
- Frontend completely unresponsive

### **Partial Rollback If:**
- Intermittent errors on specific endpoints
- Performance degradation >20%
- Specific features not working

### **Continue Debugging If:**
- <10% error rate
- Issues are localized/specific
- Core functionality working

---

**RECOMMENDATION**: Start with Phase 1 diagnostics immediately to understand the scope, then proceed based on findings. If issues are severe, do immediate conservative rollback to stable state.