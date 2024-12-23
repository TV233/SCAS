package com.kclgroup.backend.pojo.entity;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableField;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import lombok.Data;
import java.io.Serializable;
import java.time.LocalDateTime;

@Data
@TableName(value = "word_frequency")
public class WordFrequency implements Serializable {
    @TableId(type = IdType.AUTO)
    private Integer id;
    
    private String stockCode;
    private String word;
    private Integer frequency;
    private LocalDateTime updateTime;
    
    @TableField(exist = false)
    private static final long serialVersionUID = 1L;
} 