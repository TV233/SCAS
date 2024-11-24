package com.kclgroup.backend.pojo.vo;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableField;
import com.baomidou.mybatisplus.annotation.TableId;
import lombok.Data;

import java.io.Serializable;
import java.math.BigDecimal;

@Data
public class StockIndicesVo {
    private Integer id;
    private String symbol;
    private String name;
    private BigDecimal indexValue;
    private BigDecimal changePercent;
    private BigDecimal changeAmount;
}