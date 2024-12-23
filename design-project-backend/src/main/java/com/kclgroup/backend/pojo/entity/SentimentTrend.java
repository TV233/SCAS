package com.kclgroup.backend.pojo.entity;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableField;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import lombok.Data;
import java.io.Serializable;
import java.time.LocalDate;
import java.time.LocalDateTime;

@Data
@TableName(value = "sentiment_trend")
public class SentimentTrend implements Serializable {
    @TableId(type = IdType.AUTO)
    private Integer id;
    
    private String stockCode;
    private LocalDate date;
    private Float sentimentAvg;
    private Integer commentCount;
    private LocalDateTime updateTime;
    
    @TableField(exist = false)
    private static final long serialVersionUID = 1L;
} 