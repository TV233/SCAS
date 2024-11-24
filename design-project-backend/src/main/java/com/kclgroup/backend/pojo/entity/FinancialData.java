package com.kclgroup.backend.pojo.entity;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableField;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import java.io.Serializable;
import lombok.Data;

/**
 * 
 * @TableName financial_data
 */
@TableName(value ="financial_data")
@Data
public class FinancialData implements Serializable {
    /**
     * 
     */
    private String stockCode;

    /**
     * 
     */
    private String year;

    /**
     * 营业总收入
     */
    private Double totalOperatereveIncrease;

    /**
     * 归母净利润
     */
    private Double parentNetprofitIncrease;

    /**
     * 扣非归母净利润
     */
    private Double dnetprofitatpcTcalIncrease;

    /**
     * 
     */
    private String summary;

    @TableField(exist = false)
    private static final long serialVersionUID = 1L;
}