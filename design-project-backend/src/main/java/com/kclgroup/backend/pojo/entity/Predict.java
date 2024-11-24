package com.kclgroup.backend.pojo.entity;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableField;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import java.io.Serializable;
import java.math.BigDecimal;
import lombok.Data;

/**
 * 
 * @TableName predict
 */
@TableName(value ="predict")
@Data
public class Predict implements Serializable {
    /**
     * 
     */
    @TableId(type = IdType.AUTO)
    private Integer id;

    /**
     * 
     */
    private String stockCode;

    /**
     * 
     */
    private Integer ratingOrgNum;

    /**
     * 
     */
    private BigDecimal ratingBuyNum;

    /**
     * 
     */
    private BigDecimal ratingAddNum;

    /**
     * 
     */
    private BigDecimal ratingNeutralNum;

    /**
     * 
     */
    private BigDecimal ratingReduceNum;

    /**
     * 
     */
    private BigDecimal ratingSaleNum;

    /**
     * 
     */
    private Integer year1;

    /**
     * 
     */
    private BigDecimal eps1;

    /**
     * 
     */
    private Integer year2;

    /**
     * 
     */
    private BigDecimal eps2;

    /**
     * 
     */
    private Integer year3;

    /**
     * 
     */
    private BigDecimal eps3;

    /**
     * 
     */
    private Integer year4;

    /**
     * 
     */
    private BigDecimal eps4;

    @TableField(exist = false)
    private static final long serialVersionUID = 1L;
}