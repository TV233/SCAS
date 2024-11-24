package com.kclgroup.backend.pojo.vo;

import lombok.Data;

@Data
public class FinancialYearData {
    private Double totalOperatereveIncrease;
    private Double parentNetprofitIncrease;
    private Double dnetprofitatpcTcalIncrease;

    public FinancialYearData(Double totalOperatereveIncrease, Double parentNetprofitIncrease, Double dnetprofitatpcTcalIncrease) {
        this.totalOperatereveIncrease = totalOperatereveIncrease;
        this.parentNetprofitIncrease = parentNetprofitIncrease;
        this.dnetprofitatpcTcalIncrease = dnetprofitatpcTcalIncrease;
    }
    // Constructors, getters and setters
}