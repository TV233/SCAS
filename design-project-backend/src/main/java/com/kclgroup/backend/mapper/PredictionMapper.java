package com.kclgroup.backend.mapper;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.kclgroup.backend.pojo.entity.Prediction;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Select;
import java.util.List;
import java.math.BigDecimal;

@Mapper
public interface PredictionMapper extends BaseMapper<Prediction> {
    @Select("SELECT * FROM predictions WHERE stock_code = #{stockCode} ORDER BY prediction_date")
    List<Prediction> getPredictionsByStockCode(String stockCode);
    
    @Select("SELECT * FROM predictions WHERE stock_code = #{stockCode} AND model_name = #{modelName} ORDER BY prediction_date DESC LIMIT 1")
    Prediction getLatestPrediction(String stockCode, String modelName);
    
    @Select("SELECT model_name FROM predictions WHERE stock_code = #{stockCode} GROUP BY model_name ORDER BY AVG(accuracy) DESC LIMIT 1")
    String getMostAccurateModel(String stockCode);

    @Select("SELECT predicted_price FROM predictions WHERE stock_code = #{stockCode} ORDER BY prediction_date DESC LIMIT 1")
    BigDecimal getCurrentPrice(String stockCode);
} 