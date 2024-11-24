package com.kclgroup.backend.pojo.vo;

import lombok.Data;

import java.util.HashMap;
import java.util.Map;
@Data
public class FinancialDataVo {
    private String stockCode;
    private String summary;
    private Map<String, FinancialYearData> financialDataByYear;

    public FinancialDataVo(String stockCode, String summary) {
        this.stockCode = stockCode;
        this.summary = summary;
        this.financialDataByYear = new HashMap<>();
    }

    // Getters and Setters
    public String getStockCode() {
        return stockCode;
    }

    public void setStockCode(String stockCode) {
        this.stockCode = stockCode;
    }

    public String getSummary() {
        return summary;
    }

    public void setSummary(String summary) {
        this.summary = summary;
    }

    public Map<String, FinancialYearData> getFinancialDataByYear() {
        return financialDataByYear;
    }

    public void setFinancialDataByYear(Map<String, FinancialYearData> financialDataByYear) {
        this.financialDataByYear = financialDataByYear;
    }

    public void addFinancialYearData(String year, FinancialYearData data) {
        this.financialDataByYear.put(year, data);
    }
}
