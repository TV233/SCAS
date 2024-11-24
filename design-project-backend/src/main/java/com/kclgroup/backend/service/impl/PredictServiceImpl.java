package com.kclgroup.backend.service.impl;

import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.kclgroup.backend.pojo.entity.Predict;
import com.kclgroup.backend.pojo.vo.PredictVo;
import com.kclgroup.backend.service.PredictService;
import com.kclgroup.backend.mapper.PredictMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.math.BigDecimal;
import java.util.List;

/**
* @author 张小明
* @description 针对表【predict】的数据库操作Service实现
* @createDate 2024-06-24 21:18:07
*/
@Service
public class PredictServiceImpl extends ServiceImpl<PredictMapper, Predict>
    implements PredictService{

    @Autowired PredictMapper predictMapper;
    @Override
    public List<PredictVo> getPredict() {
        List<PredictVo> predictVo = predictMapper.getPredict();
        return predictVo;
    }

    @Override
    public Integer getRatingOrgNum(String stockCode) {
        Integer ratingOrgNum = predictMapper.getRatingOrgNum(stockCode);
        return ratingOrgNum;
    }

    @Override
    public BigDecimal getRatingBuyNum(String stockCode) {
        BigDecimal ratingBuyNum = predictMapper.getRatingBuyNum(stockCode);
        return ratingBuyNum;
    }

    @Override
    public BigDecimal getRatingAddNum(String stockCode) {
        BigDecimal ratingAddNum = predictMapper.getRatingAddNum(stockCode);
        return ratingAddNum;
    }

    @Override
    public BigDecimal getRatingSaleNum(String stockCode) {
        BigDecimal ratingSaleNum = predictMapper.getRatingSaleNum(stockCode);
        return ratingSaleNum;
    }

    @Override
    public BigDecimal getRatingNeutralNum(String stockCode) {
        BigDecimal ratingNeutralNum = predictMapper.getRatingNeutralNum(stockCode);
        return ratingNeutralNum;
    }

    @Override
    public BigDecimal getRatingReduceNum(String stockCode) {
        BigDecimal ratingReduceNum = predictMapper.getRatingReduceNum(stockCode);
        return ratingReduceNum;
    }

    @Override
    public Integer getYear1(String stockCode) {
        Integer year1 = predictMapper.getYear1(stockCode);
        return year1;
    }

    @Override
    public BigDecimal getEps1(String stockCode) {
        BigDecimal eps1 = predictMapper.getEps1(stockCode);
        return eps1;
    }

    @Override
    public Integer getYear2(String stockCode) {
        Integer year2 = predictMapper.getYear2(stockCode);
        return year2;
    }

    @Override
    public BigDecimal getEps2(String stockCode) {
        BigDecimal eps2 = predictMapper.getEps2(stockCode);
        return eps2;
    }

    @Override
    public Integer getYear3(String stockCode) {
        Integer year3 = predictMapper.getYear3(stockCode);
        return year3;
    }

    @Override
    public BigDecimal getEps3(String stockCode) {
        BigDecimal eps3 = predictMapper.getEps3(stockCode);
        return eps3;
    }

    @Override
    public Integer getYear4(String stockCode) {
        Integer year4 = predictMapper.getYear4(stockCode);
        return year4;
    }

    @Override
    public BigDecimal getEps4(String stockCode) {
        BigDecimal eps4 = predictMapper.getEps4(stockCode);
        return eps4;
    }
}




